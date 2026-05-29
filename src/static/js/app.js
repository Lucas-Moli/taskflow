(function () {
    function openModal(id) {
        const modal = document.getElementById(id);
        if (!modal) return;
        modal.classList.add('open');
        modal.setAttribute('aria-hidden', 'false');
        document.body.classList.add('overflow-hidden');
    }

    function closeModal(id) {
        const modal = document.getElementById(id);
        if (!modal) return;
        modal.classList.remove('open');
        modal.setAttribute('aria-hidden', 'true');
        if (!document.querySelector('[data-modal].open')) {
            document.body.classList.remove('overflow-hidden');
        }
    }

    window.toggleModal = function (modalId) {
        const modal = document.getElementById(modalId);
        if (!modal) return;
        if (modal.classList.contains('open')) {
            closeModal(modalId);
        } else {
            openModal(modalId);
        }
    };

    window.openEditModal = function (id, title, description, priority, status) {
        const form = document.getElementById('edit-form');
        if (!form) return;
        form.action = `/task/update/${id}`;
        document.getElementById('edit-title').value = title;
        document.getElementById('edit-description').value = description;
        document.getElementById('edit-priority').value = priority;
        document.getElementById('edit-status').value = status;
        openModal('edit-modal');
    };

    document.querySelectorAll('[data-modal-panel]').forEach((panel) => {
        panel.addEventListener('click', (e) => e.stopPropagation());
    });

    document.querySelectorAll('[data-modal]').forEach((modal) => {
        modal.addEventListener('click', () => closeModal(modal.id));
        modal.querySelectorAll('[data-modal-close]').forEach((btn) => {
            btn.addEventListener('click', () => closeModal(modal.id));
        });
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            document.querySelectorAll('[data-modal].open').forEach((modal) => {
                closeModal(modal.id);
            });
        }
    });
})();
