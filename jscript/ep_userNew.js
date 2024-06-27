  function toggleLabel() {
    const checkbox = document.getElementById('ext');
    const label = document.getElementById('nameLabel');
    if (checkbox.checked) {
      label.textContent = 'Имя Отчество Фамилия';
    } else {
      label.textContent = 'Фамилия Имя Отчество';
    }
  }

  function clearInputField() {
    document.getElementById('fullName').value = '';
  }

function copyToClipboard(elementId) {
  const element = document.getElementById(elementId);
  let textToCopy;

  // проверяем, является ли элемент полем ввода
  if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
    textToCopy = element.value; // полe input
  } else {
    textToCopy = element.textContent; // иначе текстовое содержимое элемента
  }

  navigator.clipboard.writeText(textToCopy)
    .then(() => {
      // действие после успешного копирования
    })
    .catch(err => {
      // обработка ошибки
    });
}

  function transliterate() {
    const fullName = document.getElementById('fullName').value;
    const fullNameSur = fullName.trim().split(/\s+/);

    if (fullNameSur.length !== 3) {
      alert('Поле должно содержать три слова');
      return;
    }

    for (let i = 0; i < fullNameSur.length; i++) {
      fullNameSur[i] = capLetter(fullNameSur[i]);
    }

    const fullNameCap = fullNameSur.join(' ');
    document.getElementById('fullName').value = fullNameCap;

    const isChecked = document.getElementById('ext').checked;
      if (isChecked) {
        // Имя Отчество Фамилия
        name = fullNameSur[0];
        patronymic = fullNameSur[1];
        surname = fullNameSur[2];
      } else {
        // Фамилия Имя Отчество
        surname = fullNameSur[0];
        name = fullNameSur[1];
        patronymic = fullNameSur[2];
      }

    document.getElementById('surname').textContent = surname;
    document.getElementById('name').textContent = name;
    document.getElementById('patronymic').textContent = patronymic;

    document.getElementById('copyFIOButton').textContent = `${surname} ${name} ${patronymic}`;
    document.getElementById('copyIOFButton').textContent = `${name} ${patronymic} ${surname}`;

    document.getElementById('password').value = 'xxxxx123';

    // логин с учетом состояния чекбокса
      const login = 'ep.' + transliterateText(surname.toLowerCase()) +
                    transliterateText(name.charAt(0).toLowerCase()) +
                    transliterateText(patronymic.charAt(0).toLowerCase());
      document.getElementById('login').textContent = login;
  }

  function capLetter(text) {
    if (typeof text === 'string' && text !== '') {
      return text.charAt(0).toUpperCase() + text.slice(1).toLowerCase();
    } else {
      return '';
    }
  }

  function transliterateText(text) {
    const map = {
      'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E', 'Ж': 'ZH', 'З': 'Z',
      'И': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R',
      'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'KH', 'Ц': 'TS', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHCH',
      'Ъ': 'IE', 'Ы': 'Y', 'Э': 'E', 'Ю': 'IU', 'Я': 'IA', 'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g',
      'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l',
      'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f',
      'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ъ': 'ie', 'ы': 'y', 'э': 'e',
      'ю': 'iu', 'я': 'ia', 'Ь': '', 'ь': ''
    };

    let transliteratedText = '';
    for (let i = 0; i < text.length; i++) {
      const char = text[i];
      const transliteratedChar = map[char] || char;
      transliteratedText += transliteratedChar;
    }

    return transliteratedText;
  }
