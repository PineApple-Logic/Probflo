class ContextMenu {
  constructor(elementId, options) {
    this.element = document.getElementById(elementId);
    this.menu = this.createContextMenu(options);

    this.element.addEventListener('contextmenu', (event) => {
      event.preventDefault();
      this.showContextMenu(event.clientX, event.clientY);
    });
  }

  createContextMenu(options) {
    const menu = document.createElement('div');
    menu.classList.add('context-menu');
    
    const ul = document.createElement('ul');
    options.forEach((option, index) => {
      const li = document.createElement('li');
      li.innerHTML = `
        <span>${option.label}</span>
        <span class="shortcut">${option.shortcut || ''}</span>
      `;
      
      li.addEventListener('click', () => option.handler(index));
      ul.appendChild(li);
    });

    menu.appendChild(ul);
    document.body.appendChild(menu);
    return menu;
  }

  showContextMenu(x, y) {
    this.menu.style.display = 'block';
    this.menu.style.left = x + 'px';
    this.menu.style.top = y + 'px';

    document.addEventListener('click', this.closeContextMenu.bind(this));
    document.addEventListener('keydown', this.handleKeyboardShortcut.bind(this));
  }

  closeContextMenu() {
    this.menu.style.display = 'none';
    document.removeEventListener('click', this.closeContextMenu.bind(this));
    document.removeEventListener('keydown', this.handleKeyboardShortcut.bind(this));
  }

  handleKeyboardShortcut(event) {
    const shortcutKey = event.key.toLowerCase();
    const shortcutItem = Array.from(this.menu.querySelectorAll('li')).find((item) => {
      const shortcutSpan = item.querySelector('.shortcut');
      return shortcutSpan && shortcutSpan.textContent.toLowerCase().includes(shortcutKey);
    });

    if (shortcutItem) {
      shortcutItem.click();
    }
  }
}