(() => {
  const tg = window.Telegram && window.Telegram.WebApp ? window.Telegram.WebApp : null;
  if (tg) {
    tg.ready();
    tg.expand();
    try { tg.setHeaderColor('#f7f6f2'); tg.setBackgroundColor('#f7f6f2'); } catch (_) {}
  }
  const translations = {
    uz: {
      delivery: 'Butun O‘zbekiston bo‘ylab', heroEyebrow: 'YANGI MAVSUM · 2026', heroTitle: 'Uslub — bu<br><em>o‘zing bo‘lish.</em>', heroText: 'Har kun uchun tanlangan kiyimlar. Soddalik, sifat va o‘ziga xoslik bir joyda.', heroCta: 'Kolleksiyani ko‘rish', heroFoot: 'YANGI KELGANLAR', heroCaption: 'CITY ESSENTIALS', collectionEyebrow: 'SIZ UCHUN TANLANDI', collectionTitle: 'Kashf eting<span class="brand-dot">.</span>', collectionText: 'Sevimli obrazingizni toping — qolganini bizga qo‘ying.', searchPlaceholder: 'Mahsulot qidirish...', sortLabel: 'Saralash:', sortPopular: 'Tavsiya etilgan', sortLow: 'Arzonidan', sortHigh: 'Qimmatidan', sortNew: 'Yangilari', clearFilters: 'Filtrlarni tozalash ×', loading: 'Katalog yuklanmoqda...', promoEyebrow: 'MODA COMMUNITY', promoTitle: 'Kamroq, lekin yaxshiroq.', promoText: 'Uzoq vaqt kiyiladigan, o‘zingizga mos tanlovlar.', promoCta: 'Katalogga qaytish', footerText: 'Yaxshi uslub — mayda detallardan boshlanadi.', navShop: 'Do‘kon', navSaved: 'Saqlangan', navCart: 'Savatcha', all: 'Hammasi', women: 'Ayollar', men: 'Erkaklar', accessories: 'Aksessuarlar', shoes: 'Oyoq kiyim', favorites: 'Sevimlilar', result: 'ta mahsulot', noResults: 'Hech narsa topilmadi', noResultsText: 'Qidiruv so‘zini yoki filtrlarni o‘zgartirib ko‘ring.', new: 'YANGI', sale: 'CHEGIRMA', add: 'Savatchaga', details: 'Batafsil', stock: 'Mavjud', size: 'O‘lcham', color: 'Rang', chooseSize: 'O‘lchamni tanlang', chooseColor: 'Rangni tanlang', addSuccess: 'Mahsulot savatchaga qo‘shildi', favAdded: 'Sevimlilarga saqlandi', favRemoved: 'Sevimlilardan olib tashlandi', cartTitle: 'Savatcha', emptyCart: 'Savatchangiz hozircha bo‘sh', emptyCartText: 'Yoqtirgan mahsulotlaringizni tanlab, shu yerga qo‘shing.', continue: 'Xaridni davom ettirish', subtotal: 'Jami summa', name: 'Ismingiz', phone: 'Telefon raqamingiz', address: 'Yetkazib berish manzili', note: 'Izoh (ixtiyoriy)', sendOrder: 'Buyurtma so‘rovini yuborish', noPayment: 'To‘lov olinmaydi — bu faqat buyurtma so‘rovi.', required: 'Ism, telefon va manzilni to‘ldiring.', telegramOnly: 'Buyurtmani yuborish uchun Mini App’ni Telegram bot ichidan oching.', orderSuccess: 'So‘rovingiz yuborildi! Buyurtma №', orderError: 'Buyurtmani yuborib bo‘lmadi. Qayta urinib ko‘ring.', catalogError: 'Katalog yuklanmadi. Sahifani yangilang.', currency: 'so‘m', item: 'dona', languageChanged: 'Til o‘zgartirildi: O‘zbekcha', close: 'Yopish', remove: 'Olib tashlash'
    },
    ru: {
      delivery: 'Доставка по всему Узбекистану', heroEyebrow: 'НОВЫЙ СЕЗОН · 2026', heroTitle: 'Стиль — это<br><em>быть собой.</em>', heroText: 'Одежда на каждый день. Простота, качество и индивидуальность в одном месте.', heroCta: 'Смотреть коллекцию', heroFoot: 'НОВИНКИ', heroCaption: 'CITY ESSENTIALS', collectionEyebrow: 'ПОДОБРАНО ДЛЯ ВАС', collectionTitle: 'Откройте<span class="brand-dot">.</span>', collectionText: 'Найдите свой образ — остальное мы оставим простым.', searchPlaceholder: 'Поиск товаров...', sortLabel: 'Сортировка:', sortPopular: 'Рекомендуемые', sortLow: 'Сначала дешевле', sortHigh: 'Сначала дороже', sortNew: 'Сначала новинки', clearFilters: 'Сбросить фильтры ×', loading: 'Загружаем каталог...', promoEyebrow: 'MODA COMMUNITY', promoTitle: 'Меньше, но лучше.', promoText: 'Продуманные вещи, которые хочется носить долго.', promoCta: 'Вернуться в каталог', footerText: 'Хороший стиль начинается с деталей.', navShop: 'Магазин', navSaved: 'Избранное', navCart: 'Корзина', all: 'Все товары', women: 'Женское', men: 'Мужское', accessories: 'Аксессуары', shoes: 'Обувь', favorites: 'Избранное', result: 'товаров', noResults: 'Ничего не найдено', noResultsText: 'Попробуйте изменить запрос или фильтры.', new: 'NEW', sale: 'СКИДКА', add: 'В корзину', details: 'Подробнее', stock: 'В наличии', size: 'Размер', color: 'Цвет', chooseSize: 'Выберите размер', chooseColor: 'Выберите цвет', addSuccess: 'Товар добавлен в корзину', favAdded: 'Добавлено в избранное', favRemoved: 'Удалено из избранного', cartTitle: 'Корзина', emptyCart: 'Ваша корзина пока пуста', emptyCartText: 'Выберите понравившиеся товары — они появятся здесь.', continue: 'Продолжить покупки', subtotal: 'Итого', name: 'Ваше имя', phone: 'Номер телефона', address: 'Адрес доставки', note: 'Комментарий (необязательно)', sendOrder: 'Отправить заявку', noPayment: 'Оплата не взимается — это только заявка на заказ.', required: 'Заполните имя, телефон и адрес.', telegramOnly: 'Чтобы отправить заказ, откройте Mini App из Telegram-бота.', orderSuccess: 'Заявка отправлена! Номер заказа: ', orderError: 'Не удалось отправить заявку. Попробуйте ещё раз.', catalogError: 'Не удалось загрузить каталог. Обновите страницу.', currency: 'сум', item: 'шт.', languageChanged: 'Язык изменён: Русский', close: 'Закрыть', remove: 'Удалить'
    }
  };
  const categories = ['all', 'women', 'men', 'accessories', 'shoes'];
  const $ = (selector, parent = document) => parent.querySelector(selector);
  const $$ = (selector, parent = document) => Array.from(parent.querySelectorAll(selector));
  const safeRead = (key, fallback) => { try { const value = localStorage.getItem(key); return value ? JSON.parse(value) : fallback; } catch (_) { return fallback; } };
  let lang = localStorage.getItem('moda-language') || ((tg && tg.initDataUnsafe && tg.initDataUnsafe.user && (tg.initDataUnsafe.user.language_code || '').startsWith('ru')) ? 'ru' : 'uz');
  let products = [];
  let selectedCategory = 'all';
  let searchTerm = '';
  let sortMode = 'popular';
  let viewMode = 'catalog';
  let favorites = safeRead('moda-favorites', []);
  let cart = safeRead('moda-cart', []);
  let selectedProduct = null;
  let selectedSize = '';
  let selectedColor = '';
  let toastTimer = null;
  const t = (key) => (translations[lang] && translations[lang][key]) || translations.uz[key] || key;
  const esc = (value) => String(value ?? '').replace(/[&<>"']/g, (char) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
  const price = (value) => `${Number(value).toLocaleString(lang === 'ru' ? 'ru-RU' : 'uz-UZ')} ${t('currency')}`;
  const pName = (product) => product.name[lang] || product.name.uz;
  const pDescription = (product) => product.description[lang] || product.description.uz;
  const categoryName = (category) => t(category);

  function applyTranslations() {
    document.documentElement.lang = lang;
    $$('[data-i18n]').forEach((node) => { node.innerHTML = t(node.dataset.i18n); });
    $$('[data-i18n-placeholder]').forEach((node) => { node.placeholder = t(node.dataset.i18nPlaceholder); });
    const langButton = $('.lang-toggle');
    if (langButton) langButton.innerHTML = `${lang.toUpperCase()} <span>⌄</span>`;
  }
  function showToast(message) {
    const node = $('#toast'); node.textContent = message; node.classList.add('show');
    clearTimeout(toastTimer); toastTimer = setTimeout(() => node.classList.remove('show'), 2800);
  }
  function saveCart() { localStorage.setItem('moda-cart', JSON.stringify(cart)); renderCartCount(); }
  function renderCartCount() {
    const count = cart.reduce((sum, item) => sum + item.quantity, 0);
    $('#cart-count').textContent = count; $('#nav-cart-count').textContent = count;
  }
  function renderCategories() {
    $('#categories').innerHTML = categories.map((category) => `<button class="category-chip ${selectedCategory === category && viewMode === 'catalog' ? 'active' : ''}" data-action="category" data-category="${category}">${esc(categoryName(category))}</button>`).join('');
  }
  function visibleProducts() {
    let items = [...products];
    if (viewMode === 'favorites') items = items.filter((product) => favorites.includes(product.id));
    if (selectedCategory !== 'all' && viewMode === 'catalog') items = items.filter((product) => product.category === selectedCategory);
    if (searchTerm) {
      const query = searchTerm.toLocaleLowerCase();
      items = items.filter((product) => `${pName(product)} ${pDescription(product)} ${product.category}`.toLocaleLowerCase().includes(query));
    }
    if (sortMode === 'price-asc') items.sort((a,b) => a.price - b.price);
    if (sortMode === 'price-desc') items.sort((a,b) => b.price - a.price);
    if (sortMode === 'new') items.sort((a,b) => Number(b.isNew) - Number(a.isNew));
    return items;
  }
  function productCard(product, index) {
    const favorite = favorites.includes(product.id);
    const badge = product.isSale ? `<span class="product-badge sale">${t('sale')}</span>` : product.isNew ? `<span class="product-badge">${t('new')}</span>` : '';
    const oldPrice = product.oldPrice ? `<span class="old-price">${price(product.oldPrice)}</span>` : '';
    return `<article class="product-card" style="animation-delay:${Math.min(index,8)*.035}s">
      <div class="product-media" data-action="details" data-id="${esc(product.id)}" role="button" tabindex="0" aria-label="${esc(pName(product))}">
        <img src="${esc(product.image)}" alt="${esc(pName(product))}" loading="lazy" onerror="this.style.opacity='.15';this.alt='Image unavailable'">
        ${badge}<button class="favorite-button ${favorite?'active':''}" data-action="favorite" data-id="${esc(product.id)}" aria-label="${favorite?t('favRemoved'):t('favAdded')}">${favorite?'♥':'♡'}</button>
        <button class="quick-add" data-action="quick-add" data-id="${esc(product.id)}"><span>${t('add')}</span><span>＋</span></button>
      </div>
      <div class="product-info"><div class="product-meta"><span>${esc(categoryName(product.category))}</span><span class="stock-dot">● ${t('stock')}</span></div><h3 class="product-name" data-action="details" data-id="${esc(product.id)}">${esc(pName(product))}</h3><div class="price-row"><span>${price(product.price)}</span>${oldPrice}</div></div>
    </article>`;
  }
  function renderProducts() {
    const items = visibleProducts();
    $('#product-grid').innerHTML = items.length ? items.map(productCard).join('') : `<div class="empty-state"><div><strong>${t('noResults')}</strong><p>${t('noResultsText')}</p></div></div>`;
    $('#result-count').textContent = `${items.length} ${t('result')}`;
    $('#clear-filters').hidden = !(searchTerm || selectedCategory !== 'all' || viewMode === 'favorites');
    renderCategories();
  }
  function renderDetails() {
    if (!selectedProduct) return;
    const product = selectedProduct;
    const oldPrice = product.oldPrice ? `<span class="old-price">${price(product.oldPrice)}</span>` : '';
    $('#product-modal').innerHTML = `<div class="modal-image"><img src="${esc(product.image)}" alt="${esc(pName(product))}"></div><div class="modal-content">
      <button class="modal-close" data-action="close-overlays" aria-label="${t('close')}">×</button><div class="modal-category">${esc(categoryName(product.category))} / MODA STUDIO</div><h3>${esc(pName(product))}</h3><div class="modal-price">${price(product.price)} ${oldPrice}</div><p>${esc(pDescription(product))}</p>
      <div class="option-label">${t('size')} <span>${esc(selectedSize)}</span></div><div class="size-options">${product.sizes.map((size) => `<button class="size-option ${selectedSize===size?'selected':''}" data-action="size" data-size="${esc(size)}">${esc(size)}</button>`).join('')}</div>
      <div class="option-label">${t('color')} <span>${esc((product.colors.find((color) => color.id === selectedColor) || product.colors[0])[lang])}</span></div><div class="color-options">${product.colors.map((color) => `<button class="color-option ${selectedColor===color.id?'selected':''}" style="background:${esc(color.hex)}" data-action="color" data-color="${esc(color.id)}" title="${esc(color[lang])}" aria-label="${esc(color[lang])}"></button>`).join('')}</div>
      <button class="primary-button modal-add" data-action="modal-add"><span>${t('add')}</span><span>${price(product.price)}　＋</span></button><div class="stock-note">${t('stock')} · ${lang==='uz'?'Buyurtma admin tomonidan tasdiqlanadi':'Заказ подтверждает администратор'}</div>
    </div>`;
  }
  function renderCart() {
    const drawer = $('#cart-drawer');
    const lines = cart.map((item, index) => {
      const product = products.find((p) => p.id === item.productId);
      if (!product) return '';
      const color = product.colors.find((c) => c.id === item.color);
      return `<div class="cart-line"><img src="${esc(product.image)}" alt="${esc(pName(product))}"><div><div class="cart-line-name">${esc(pName(product))}</div><div class="cart-line-meta">${t('size')}: ${esc(item.size)}<br>${t('color')}: ${esc(color ? color[lang] : item.color)}</div><div class="qty-control"><button data-action="quantity" data-index="${index}" data-delta="-1" aria-label="Decrease">−</button><span>${item.quantity}</span><button data-action="quantity" data-index="${index}" data-delta="1" aria-label="Increase">＋</button></div></div><div><div class="cart-line-price">${price(product.price * item.quantity)}</div><button class="remove-item" data-action="remove-item" data-index="${index}" aria-label="${t('remove')}">×</button></div></div>`;
    }).join('');
    const total = cart.reduce((sum, item) => { const p = products.find((product) => product.id === item.productId); return sum + (p ? p.price * item.quantity : 0); }, 0);
    drawer.innerHTML = `<div class="drawer-head"><h2>${t('cartTitle')} <span>(${cart.reduce((sum,item)=>sum+item.quantity,0)} ${t('item')})</span></h2><button class="drawer-close" data-action="close-overlays" aria-label="${t('close')}">×</button></div>
      ${cart.length ? `<div class="cart-items">${lines}</div><div class="cart-footer"><div class="cart-total"><span>${t('subtotal')}</span><strong>${price(total)}</strong></div><form class="order-form" id="order-form"><input name="customerName" autocomplete="name" placeholder="${t('name')} *" minlength="2" maxlength="100" required><input name="phone" autocomplete="tel" type="tel" placeholder="${t('phone')} *" minlength="5" maxlength="40" required><input name="address" autocomplete="street-address" placeholder="${t('address')} *" minlength="4" maxlength="300" required><textarea name="note" placeholder="${t('note')}" maxlength="500"></textarea><button class="primary-button" type="submit"><span>${t('sendOrder')}</span><span>↗</span></button><p class="payment-note">${t('noPayment')}</p></form></div>` : `<div class="cart-empty"><div class="empty-icon">▱</div><b>${t('emptyCart')}</b><p>${t('emptyCartText')}</p><button class="primary-button" data-action="close-overlays">${t('continue')}　↗</button></div>`}`;
  }
  function openCart() { $('#overlay').classList.add('visible'); $('#cart-drawer').classList.add('open'); $('#product-modal').classList.remove('open'); renderCart(); }
  function openDetails(id) {
    selectedProduct = products.find((product) => product.id === id);
    if (!selectedProduct) return;
    selectedSize = selectedProduct.sizes[0]; selectedColor = selectedProduct.colors[0].id;
    renderDetails(); $('#overlay').classList.add('visible'); $('#product-modal').classList.add('open'); $('#cart-drawer').classList.remove('open');
  }
  function closeOverlays() { $('#overlay').classList.remove('visible'); $('#product-modal').classList.remove('open'); $('#cart-drawer').classList.remove('open'); }
  function addItem(product, size, color) {
    const existing = cart.find((item) => item.productId === product.id && item.size === size && item.color === color);
    if (existing) existing.quantity = Math.min(20, existing.quantity + 1);
    else cart.push({productId:product.id, quantity:1, size, color});
    saveCart(); renderCart(); showToast(t('addSuccess'));
    try { tg && tg.HapticFeedback && tg.HapticFeedback.impactOccurred('light'); } catch (_) {}
  }
  function changeLanguage() {
    lang = lang === 'uz' ? 'ru' : 'uz'; localStorage.setItem('moda-language', lang); applyTranslations(); renderProducts(); renderCartCount();
    if (selectedProduct && $('#product-modal').classList.contains('open')) renderDetails();
    if ($('#cart-drawer').classList.contains('open')) renderCart();
  }
  function setView(view) { viewMode = view; if (view === 'catalog') selectedCategory = 'all'; renderProducts(); document.querySelector('.collection-head').scrollIntoView({behavior:'smooth',block:'start'}); }

  document.addEventListener('click', (event) => {
    const target = event.target.closest('[data-action]');
    if (!target) return;
    const action = target.dataset.action;
    if (action === 'language') changeLanguage();
    else if (action === 'scroll-products' || action === 'nav-catalog') { viewMode='catalog'; selectedCategory='all'; renderProducts(); $('#products').scrollIntoView({behavior:'smooth'}); }
    else if (action === 'category') { viewMode='catalog'; selectedCategory=target.dataset.category; renderProducts(); }
    else if (action === 'clear-filters') { viewMode='catalog'; selectedCategory='all'; searchTerm=''; $('#search').value=''; renderProducts(); }
    else if (action === 'favorite') {
      const id=target.dataset.id;
      if (favorites.includes(id)) { favorites=favorites.filter((value)=>value!==id); showToast(t('favRemoved')); }
      else { favorites.push(id); showToast(t('favAdded')); }
      localStorage.setItem('moda-favorites',JSON.stringify(favorites)); renderProducts();
    }
    else if (action === 'show-favorites') { setView('favorites'); }
    else if (action === 'quick-add') { const product=products.find((p)=>p.id===target.dataset.id); if (product) addItem(product,product.sizes[0],product.colors[0].id); }
    else if (action === 'details') openDetails(target.dataset.id);
    else if (action === 'size') { selectedSize=target.dataset.size; renderDetails(); }
    else if (action === 'color') { selectedColor=target.dataset.color; renderDetails(); }
    else if (action === 'modal-add') { if(selectedProduct) addItem(selectedProduct,selectedSize,selectedColor); closeOverlays(); }
    else if (action === 'open-cart') openCart();
    else if (action === 'close-overlays') closeOverlays();
    else if (action === 'quantity') {
      const index=Number(target.dataset.index), delta=Number(target.dataset.delta);
      if(cart[index]) { cart[index].quantity+=delta; if(cart[index].quantity<=0) cart.splice(index,1); else cart[index].quantity=Math.min(20,cart[index].quantity); saveCart(); renderCart(); }
    }
    else if (action === 'remove-item') { cart.splice(Number(target.dataset.index),1); saveCart(); renderCart(); }
  });
  document.addEventListener('keydown', (event) => {
    if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === 'k') { event.preventDefault(); $('#search').focus(); }
    if (event.key === 'Escape') closeOverlays();
    const target=event.target;
    if (target && target.matches('.product-media[role="button"]') && (event.key==='Enter'||event.key===' ')) { event.preventDefault(); openDetails(target.dataset.id); }
  });
  $('#search').addEventListener('input', (event) => { searchTerm=event.target.value.trim(); renderProducts(); });
  $('#sort-select').addEventListener('change', (event) => { sortMode=event.target.value; renderProducts(); });
  document.addEventListener('submit', async (event) => {
    if (event.target.id !== 'order-form') return;
    event.preventDefault();
    if (!cart.length) return;
    if (!event.target.reportValidity()) return;
    if (!tg || !tg.initData) { showToast(t('telegramOnly')); return; }
    const form = new FormData(event.target);
    const submit = event.target.querySelector('button[type="submit"]');
    submit.disabled = true; submit.querySelector('span').textContent = lang==='uz' ? 'Yuborilmoqda...' : 'Отправка...';
    try {
      const response = await fetch('/api/orders', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({
        initData:tg.initData, customerName:form.get('customerName'), phone:form.get('phone'), address:form.get('address'), note:form.get('note'), language:lang,
        items:cart.map((item)=>({productId:item.productId,quantity:item.quantity,size:item.size,color:item.color}))
      })});
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || t('orderError'));
      cart=[]; saveCart(); closeOverlays(); renderCart(); showToast(t('orderSuccess') + data.orderId);
      try { tg.HapticFeedback && tg.HapticFeedback.notificationOccurred('success'); } catch (_) {}
    } catch (error) {
      showToast(error.message && error.message.length < 160 ? error.message : t('orderError'));
      submit.disabled = false; submit.querySelector('span').textContent = t('sendOrder');
    }
  });

  async function init() {
    applyTranslations(); renderCartCount();
    try {
      const response = await fetch('/api/products');
      if (!response.ok) throw new Error('catalog');
      products = await response.json();
      renderProducts();
    } catch (_) { $('#product-grid').innerHTML = `<div class="empty-state">${t('catalogError')}</div>`; }
  }
  init();
})();
