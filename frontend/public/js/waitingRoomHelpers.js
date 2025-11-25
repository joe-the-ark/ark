/**
 * Waiting room UX helpers for unified polling reminders.
 *
 * Provides a simple toast UI and a reminder manager that can be
 * reused across the different waiting room templates.
 */
(function (window, document) {
  if (window.WaitingRoomHelpers) {
    return;
  }

  const DEFAULT_AUTO_HIDE_MS = 8000;

  function ensureStyles() {
    if (document.getElementById('waiting-room-helpers-style')) {
      return;
    }

    const style = document.createElement('style');
    style.id = 'waiting-room-helpers-style';
    style.type = 'text/css';
    style.textContent = `
      .waiting-room-toast-container {
        position: fixed;
        bottom: 24px;
        right: 24px;
        display: flex;
        flex-direction: column;
        gap: 12px;
        z-index: 9999;
        max-width: 320px;
      }

      .waiting-room-toast {
        background: rgba(82, 206, 236, 0.95);
        color: #ffffff;
        font-family: "Lato", "Helvetica Neue", Arial, sans-serif;
        padding: 14px 18px;
        border-radius: 8px;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.15);
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 12px;
        animation: waiting-room-toast-in 200ms ease-out;
      }

      .waiting-room-toast__message {
        font-size: 14px;
        line-height: 1.4;
      }

      .waiting-room-toast__close {
        background: transparent;
        border: none;
        color: currentColor;
        font-size: 16px;
        cursor: pointer;
        line-height: 1;
      }

      @keyframes waiting-room-toast-in {
        from {
          opacity: 0;
          transform: translateY(12px);
        }
        to {
          opacity: 1;
          transform: translateY(0);
        }
      }
    `;
    document.head.appendChild(style);
  }

  function ensureContainer() {
    let container = document.querySelector('.waiting-room-toast-container');
    if (!container) {
      container = document.createElement('div');
      container.className = 'waiting-room-toast-container';
      document.body.appendChild(container);
    }
    return container;
  }

  function removeToast(element) {
    if (!element) {
      return;
    }
    const parent = element.parentElement;
    if (parent) {
      parent.removeChild(element);
    }
  }

  function showToast(message, options) {
    ensureStyles();
    const container = ensureContainer();
    const toast = document.createElement('div');
    toast.className = 'waiting-room-toast';

    const messageNode = document.createElement('div');
    messageNode.className = 'waiting-room-toast__message';
    messageNode.textContent = message;
    toast.appendChild(messageNode);

    const closeButton = document.createElement('button');
    closeButton.type = 'button';
    closeButton.className = 'waiting-room-toast__close';
    closeButton.setAttribute('aria-label', 'Close reminder');
    closeButton.textContent = '×';
    closeButton.addEventListener('click', function () {
      removeToast(toast);
    });
    toast.appendChild(closeButton);

    container.appendChild(toast);

    const autoHideMs =
      options && typeof options.autoHideMs === 'number'
        ? options.autoHideMs
        : DEFAULT_AUTO_HIDE_MS;

    if (autoHideMs > 0) {
      setTimeout(function () {
        removeToast(toast);
      }, autoHideMs);
    }

    return toast;
  }

  class ReminderManager {
    constructor(config) {
      this.message = config.message || 'Please confirm when you are ready to continue.';
      this.firstDelayMs =
        typeof config.firstDelayMs === 'number' ? config.firstDelayMs : 120000;
      this.repeatDelayMs =
        typeof config.repeatDelayMs === 'number' ? config.repeatDelayMs : 180000;
      this.maxCount =
        typeof config.maxCount === 'number' ? config.maxCount : 2;
      this.autoHideMs =
        typeof config.autoHideMs === 'number'
          ? config.autoHideMs
          : DEFAULT_AUTO_HIDE_MS;
      this.count = 0;
      this.active = true;
      this.nextReminderAt = Date.now() + this.firstDelayMs;
    }

    touch() {
      if (!this.active || this.count >= this.maxCount) {
        return;
      }
      const now = Date.now();
      if (now >= this.nextReminderAt) {
        showToast(this.message, { autoHideMs: this.autoHideMs });
        this.count += 1;
        this.nextReminderAt = now + this.repeatDelayMs;
      }
    }

    stop() {
      this.active = false;
    }

    reset() {
      this.count = 0;
      this.active = true;
      this.nextReminderAt = Date.now() + this.firstDelayMs;
    }
  }

  window.WaitingRoomHelpers = {
    showToast: showToast,
    createReminder: function (config) {
      return new ReminderManager(config || {});
    },
  };
})(window, document);

