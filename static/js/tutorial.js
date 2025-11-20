// Interactive Tutorial System for Baby Moms Care Clinic
// Rose Pink Theme

class TutorialGuide {
    constructor() {
        this.tour = null;
        this.userRole = document.body.dataset.userRole || 'mother';
        this.init();
    }

    init() {
        if (localStorage.getItem('tutorialDismissed') === 'true') {
            this.addTutorialButton();
            return;
        }
        this.loadShepherd();
    }

    loadShepherd() {
        const link = document.createElement('link');
        link.rel = 'stylesheet';
        link.href = 'https://cdn.jsdelivr.net/npm/shepherd.js@11.2.0/dist/css/shepherd.css';
        document.head.appendChild(link);

        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/shepherd.js@11.2.0/dist/js/shepherd.min.js';
        script.onload = () => this.createTour();
        document.head.appendChild(script);
    }

    createTour() {
        this.tour = new Shepherd.Tour({
            useModalOverlay: true,
            defaultStepOptions: {
                classes: 'tutorial-step',
                scrollTo: { behavior: 'smooth', block: 'center' },
                cancelIcon: { enabled: true }
            }
        });

        this.addCustomStyles();
        this.addSteps();
        this.addTutorialButton();
        
        if (localStorage.getItem('tutorialDismissed') !== 'true') {
            setTimeout(() => this.startTour(), 1000);
        }
    }

    addCustomStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .shepherd-modal-overlay-container { background: rgba(0, 0, 0, 0.5); }
            .tutorial-step { background: white; border-radius: 16px; box-shadow: 0 20px 60px rgba(225, 29, 143, 0.3); border: 2px solid #f472b6; max-width: 400px; }
            .shepherd-header { background: linear-gradient(135deg, #e11d8f 0%, #f472b6 100%); padding: 16px 20px; border-radius: 14px 14px 0 0; }
            .shepherd-title { color: white; font-size: 18px; font-weight: 600; margin: 0; }
            .shepherd-cancel-icon { color: white; opacity: 0.8; transition: opacity 0.2s; }
            .shepherd-cancel-icon:hover { opacity: 1; }
            .shepherd-text { padding: 20px; color: #475569; font-size: 15px; line-height: 1.6; }
            .shepherd-footer { padding: 16px 20px; border-top: 1px solid #fce7f3; display: flex; justify-content: space-between; align-items: center; gap: 12px; }
            .shepherd-button { background: linear-gradient(135deg, #e11d8f 0%, #f472b6 100%); color: white; border: none; padding: 10px 20px; border-radius: 8px; font-weight: 600; cursor: pointer; transition: all 0.3s ease; font-size: 14px; }
            .shepherd-button:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(225, 29, 143, 0.3); }
            .shepherd-button-secondary { background: white; color: #e11d8f; border: 2px solid #e11d8f; }
            .shepherd-button-secondary:hover { background: #fef2f2; }
            .shepherd-element { z-index: 9999; position: relative; border-radius: 8px; box-shadow: 0 0 0 4px rgba(244, 114, 182, 0.5); animation: pulse-highlight 2s infinite; }
            @keyframes pulse-highlight { 0%, 100% { box-shadow: 0 0 0 4px rgba(244, 114, 182, 0.5); } 50% { box-shadow: 0 0 0 8px rgba(244, 114, 182, 0.3); } }
            .tutorial-checkbox { display: flex; align-items: center; gap: 8px; padding: 12px; background: #fef2f2; border-radius: 8px; margin-top: 12px; }
            .tutorial-checkbox input[type="checkbox"] { width: 18px; height: 18px; accent-color: #e11d8f; cursor: pointer; }
            .tutorial-checkbox label { color: #e11d8f; font-size: 13px; font-weight: 500; cursor: pointer; user-select: none; }
            #tutorial-float-btn { position: fixed; bottom: 2rem; left: 2rem; z-index: 1000; background: linear-gradient(135deg, #e11d8f 0%, #f472b6 100%); color: white; border: none; padding: 14px 24px; border-radius: 50px; font-weight: 600; cursor: pointer; box-shadow: 0 8px 25px rgba(225, 29, 143, 0.4); display: flex; align-items: center; gap: 8px; transition: all 0.3s ease; animation: float 3s ease-in-out infinite; }
            #tutorial-float-btn:hover { transform: translateY(-4px); box-shadow: 0 12px 35px rgba(225, 29, 143, 0.5); }
            #tutorial-float-btn svg { width: 20px; height: 20px; }
            @keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-10px); } }
            @media (max-width: 640px) { .tutorial-step { max-width: 90vw; } #tutorial-float-btn { padding: 12px 16px; font-size: 14px; } }
        `;
        document.head.appendChild(style);
    }

    addSteps() {
        const steps = this.getStepsForRole();
        steps.forEach((step, index) => {
            const isLastStep = index === steps.length - 1;
            this.tour.addStep({
                id: `step-${index}`,
                title: step.title,
                text: step.text + (isLastStep ? this.getDismissCheckbox() : ''),
                attachTo: { element: step.element, on: step.position || 'bottom' },
                buttons: this.getStepButtons(index, steps.length, isLastStep),
                when: {
                    show: () => {
                        const element = document.querySelector(step.element);
                        if (element) element.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                }
            });
        });
    }

    getStepsForRole() {
        const commonSteps = [
            { title: '👋 Welcome to Baby Moms Care Clinic!', text: 'Let me show you around! This quick tour will help you navigate the platform and discover all the features available to you.', element: 'nav', position: 'bottom' },
            { title: '🏠 Home Dashboard', text: 'Click here anytime to return to your main dashboard where you can see your overview and quick stats.', element: 'a[href*="dashboard"]', position: 'bottom' },
            { title: '📅 Appointments', text: 'Manage all your appointments here. Book new appointments, view upcoming visits, and track your appointment history.', element: 'a[href*="appointments"]', position: 'bottom' },
            { title: '🔔 Notifications', text: 'Stay updated with important alerts, appointment reminders, and system notifications. The red dot indicates unread notifications.', element: 'a[href*="notifications"]', position: 'bottom' },
            { title: '👤 Your Profile', text: 'Access your profile settings, update personal information, change your password, and manage your account preferences.', element: '.group button', position: 'bottom' }
        ];

        const roleSteps = {
            mother: [
                { title: '🤰 Quick Actions', text: 'These cards provide quick access to your most-used features. Click any card to jump directly to that section.', element: '.feature-card', position: 'top' },
                { title: '📊 Your Statistics', text: 'View your important stats at a glance - upcoming appointments, health records, and notifications all in one place.', element: '.clinic-stat-card', position: 'top' }
            ],
            doctor: [
                { title: '👥 Patient Management', text: 'Access your patient list, review medical records, and manage consultations from these quick action cards.', element: '.feature-card', position: 'top' },
                { title: '📊 Today\'s Overview', text: 'Monitor today\'s appointments, upcoming schedules, and patient notifications at a glance.', element: '.clinic-stat-card', position: 'top' }
            ],
            admin: [
                { title: '⚙️ Admin Controls', text: 'Manage users, monitor appointments, view reports, and configure system settings from these admin panels.', element: '.feature-card', position: 'top' },
                { title: '📊 System Statistics', text: 'Track total users, pending appointments, and system activity with these real-time statistics.', element: '.clinic-stat-card', position: 'top' }
            ]
        };

        return [...commonSteps, ...(roleSteps[this.userRole] || roleSteps.mother), 
            { title: '🎉 You\'re All Set!', text: 'You\'ve completed the tour! You can restart this tutorial anytime by clicking the "Start Tutorial" button. Enjoy using Baby Moms Care Clinic!', element: 'body', position: 'center' }
        ];
    }

    getStepButtons(index, totalSteps, isLastStep) {
        const buttons = [];
        if (index > 0) buttons.push({ text: '← Back', classes: 'shepherd-button-secondary', action: this.tour.back });
        if (!isLastStep) {
            buttons.push({ text: 'Next →', action: this.tour.next });
        } else {
            buttons.push({
                text: 'Finish',
                action: () => {
                    const checkbox = document.getElementById('dont-show-again');
                    if (checkbox && checkbox.checked) localStorage.setItem('tutorialDismissed', 'true');
                    this.tour.complete();
                }
            });
        }
        return buttons;
    }

    getDismissCheckbox() {
        return '<div class="tutorial-checkbox"><input type="checkbox" id="dont-show-again"><label for="dont-show-again">Don\'t show this tutorial again</label></div>';
    }

    addTutorialButton() {
        const button = document.createElement('button');
        button.id = 'tutorial-float-btn';
        button.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path></svg><span>Start Tutorial</span>';
        button.onclick = () => this.startTour();
        document.body.appendChild(button);
    }

    startTour() {
        if (this.tour) this.tour.start();
    }
}

if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => new TutorialGuide());
} else {
    new TutorialGuide();
}
