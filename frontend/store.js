/**
 * INFRAcare Unified Shared Data Store
 * Provides persistent, cross-page & cross-tab synchronization
 * with seamless fallback for Vercel static hosting and local FastAPI backend.
 */
(function(window) {
  const STORAGE_KEY = 'infracare_reports_v2';
  const syncChannel = ('BroadcastChannel' in window) ? new BroadcastChannel('infracare_sync_channel') : null;

  const DEFAULT_DEMO_REPORTS = [
    {
      id: 1,
      title: "Severe Pothole & Caved Asphalt",
      description: "Large 3ft crater on Outer Circle causing hazardous traffic slowdown and bike skids.",
      category: "Road",
      severity: "Critical",
      priority: "P1",
      status: "reported",
      latitude: 28.6328,
      longitude: 77.2195,
      landmark: "Outer Circle, Connaught Place, New Delhi",
      image_url: "https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=600&auto=format&fit=crop&q=80",
      support_count: 10,
      assigned_officer_id: null,
      created_at: new Date(Date.now() - 3600000 * 4).toISOString()
    },
    {
      id: 2,
      title: "Structural Crack on Pedestrian Overbridge",
      description: "Expansion joint separation and visible concrete spalling on stairs.",
      category: "Bridge",
      severity: "High",
      priority: "P2",
      status: "verified",
      latitude: 28.6289,
      longitude: 77.2145,
      landmark: "Janpath Crossing, New Delhi",
      image_url: "https://images.unsplash.com/photo-1541888946425-d0fbb186f5f7?w=600&auto=format&fit=crop&q=80",
      support_count: 14,
      assigned_officer_id: null,
      created_at: new Date(Date.now() - 3600000 * 8).toISOString()
    },
    {
      id: 3,
      title: "Streetlight Cluster Blackout (4 Poles)",
      description: "Four consecutive light poles non-functional near Janpath crossing, zero nighttime visibility.",
      category: "Lighting",
      severity: "Medium",
      priority: "P3",
      status: "assigned",
      latitude: 28.6255,
      longitude: 77.2185,
      landmark: "KG Marg & Tolstoy Rd, New Delhi",
      image_url: "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?w=600&auto=format&fit=crop&q=80",
      support_count: 3,
      assigned_officer_id: 3,
      created_at: new Date(Date.now() - 3600000 * 12).toISOString()
    },
    {
      id: 4,
      title: "Water Main Rupture & Street Flooding",
      description: "High-pressure pipeline burst leaking clean drinking water onto asphalt and sidewalk.",
      category: "Water",
      severity: "Critical",
      priority: "P1",
      status: "in_progress",
      latitude: 28.6350,
      longitude: 77.2220,
      landmark: "Barakhamba Road Junction, New Delhi",
      image_url: "https://images.unsplash.com/photo-1584467735815-f778f274e296?w=600&auto=format&fit=crop&q=80",
      support_count: 22,
      assigned_officer_id: 1,
      created_at: new Date(Date.now() - 3600000 * 18).toISOString()
    },
    {
      id: 5,
      title: "Overflowing Municipal Garbage Dump",
      description: "Community waste bin uncleared for 4 days, encroaching pedestrian pathway.",
      category: "Waste",
      severity: "Low",
      priority: "P4",
      status: "resolved",
      latitude: 28.6295,
      longitude: 77.2250,
      landmark: "Mandi House Circle, New Delhi",
      image_url: "https://images.unsplash.com/photo-1605600659873-d808a13e4d2a?w=600&auto=format&fit=crop&q=80",
      support_count: 5,
      assigned_officer_id: 2,
      created_at: new Date(Date.now() - 3600000 * 24).toISOString()
    },
    {
      id: 6,
      title: "Damaged Storm Drain Grate",
      description: "Broken cast iron drain cover leaving open 2ft pit on bicycle lane.",
      category: "Road",
      severity: "High",
      priority: "P2",
      status: "reported",
      latitude: 28.6310,
      longitude: 77.2110,
      landmark: "Baba Kharak Singh Marg, New Delhi",
      image_url: "https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=600&auto=format&fit=crop&q=80",
      support_count: 8,
      assigned_officer_id: null,
      created_at: new Date(Date.now() - 3600000 * 30).toISOString()
    }
  ];

  window.InfracareStore = {
    getReports: function() {
      try {
        const raw = localStorage.getItem(STORAGE_KEY);
        if (!raw) {
          localStorage.setItem(STORAGE_KEY, JSON.stringify(DEFAULT_DEMO_REPORTS));
          return [...DEFAULT_DEMO_REPORTS];
        }
        const parsed = JSON.parse(raw);
        if (Array.isArray(parsed) && parsed.length > 0) return parsed;
        localStorage.setItem(STORAGE_KEY, JSON.stringify(DEFAULT_DEMO_REPORTS));
        return [...DEFAULT_DEMO_REPORTS];
      } catch (e) {
        return [...DEFAULT_DEMO_REPORTS];
      }
    },

    saveReports: function(reports) {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(reports));
        if (syncChannel) syncChannel.postMessage({ type: 'STORE_UPDATED', timestamp: Date.now() });
      } catch (e) {
        console.warn('Storage save warning:', e);
      }
    },

    addReport: function(data) {
      const reports = this.getReports();
      const nextId = reports.length ? Math.max(...reports.map(r => Number(r.id) || 0)) + 1 : 1;
      const prio = data.severity === 'Critical' ? 'P1' : data.severity === 'High' ? 'P2' : data.severity === 'Medium' ? 'P3' : 'P4';

      const newReport = {
        id: nextId,
        title: data.title || 'Untitled Hazard',
        description: data.description || '',
        category: data.category || 'Road',
        severity: data.severity || 'Critical',
        priority: prio,
        status: 'reported',
        latitude: Number(data.latitude) || 28.6315,
        longitude: Number(data.longitude) || 77.2167,
        landmark: data.landmark || 'Connaught Place, New Delhi',
        image_url: data.image_url || 'https://images.unsplash.com/photo-1515162816999-a0c47dc192f7?w=600&auto=format&fit=crop&q=80',
        support_count: 1,
        assigned_officer_id: null,
        created_at: new Date().toISOString()
      };

      reports.unshift(newReport);
      this.saveReports(reports);
      return newReport;
    },

    updateStatus: function(reportId, newStatus) {
      const reports = this.getReports();
      const r = reports.find(item => Number(item.id) === Number(reportId));
      if (r) {
        r.status = newStatus;
        this.saveReports(reports);
        return true;
      }
      return false;
    },

    assignOfficer: function(reportId, officerId) {
      const reports = this.getReports();
      const r = reports.find(item => Number(item.id) === Number(reportId));
      if (r) {
        r.assigned_officer_id = Number(officerId);
        r.status = 'assigned';
        this.saveReports(reports);
        return true;
      }
      return false;
    },

    addSupport: function(reportId) {
      const reports = this.getReports();
      const r = reports.find(item => Number(item.id) === Number(reportId));
      if (r) {
        r.support_count = (r.support_count || 0) + 1;
        this.saveReports(reports);
        return r.support_count;
      }
      return 1;
    },

    onSync: function(callback) {
      if (syncChannel) {
        syncChannel.addEventListener('message', () => callback());
      }
      window.addEventListener('storage', (e) => {
        if (e.key === STORAGE_KEY) callback();
      });
    }
  };
})(window);
