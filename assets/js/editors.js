document.addEventListener('DOMContentLoaded', () => {
    // 1. Mapeo de caracteres (Alfabeto normal vs Unicode)
    const alfabetos = {
        // Referencia base para el mapeo
        normal: "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",

        // Negrita (Mathematical Bold Sans-Serif)
        negrita: "𝗮𝗯𝗰𝗱𝗲𝗳𝗴𝗵𝗶𝗷𝗸𝗹𝗺𝗻𝗼𝗽𝗾𝗿𝘀𝘁𝘂𝘃𝘄𝘅𝘆𝘇𝗔𝗕𝗖𝗗𝗘𝗙𝗚𝗛𝗜𝗝𝗞𝗟𝗠𝗡𝗢𝗣𝗤𝗥𝗦𝗧𝗨𝗩𝗪𝗫𝗬𝗭𝟬𝟭𝟮𝟯𝟰𝟱𝟲𝟳𝟴𝟵",

        // Cursiva (Mathematical Italic Sans-Serif)
        // Nota: Los números en cursiva matemática no existen como bloque único en muchos sistemas, 
        // por lo que se suelen mantener los normales o usar el bloque Serif.
        cursiva: "𝘢𝘣𝘤𝘥𝘦𝘧𝘨𝘩𝘪𝘫𝘬𝘭𝘮𝘯𝘰𝘱𝘲𝘳𝘴𝘵𝘶𝘷𝘸𝘹𝘺𝘻𝘈𝘉𝘊𝘋𝘌𝘍𝘎𝘏𝘐𝘑𝘒𝘓𝘔𝘕𝘖𝘗𝘘𝘙𝘚𝘛𝘜𝘝𝘞𝘟𝘠𝘡0123456789",
        // Negrita Cursiva (Mathematical Bold Italic Sans-Serif)
        negritaCursiva: "𝙖𝙗𝙘𝙙𝙚𝙛𝙜𝙝𝙞𝙟𝙠𝙡𝙢𝙣𝙤𝙥𝙦𝙧𝙨𝙩𝙪𝙫𝙬𝙭𝙮𝙯𝘼𝘽𝘾𝘿𝙀𝙁𝙂𝙃𝙄𝙅𝙆𝙇𝙈𝙉𝙊𝙋𝙌𝙍𝙎𝙏𝙐𝙑𝙒𝙓𝙔𝙕0123456789",

        // Invertido (Mapeo de caracteres espejo)
        invertido: {
            "a":"ɐ","b":"q","c":"ɔ","d":"p","e":"ǝ","f":"ɟ","g":"ƃ","h":"ɥ","i":"ᴉ","j":"ɾ","k":"ʞ",
            "l":"l","m":"ɯ","n":"u","o":"o","p":"d","q":"b","r":"ɹ","s":"s","t":"ʇ","u":"n","v":"ʌ",
            "w":"ʍ","x":"x","y":"ʎ","z":"z",
            "A":"∀","B":"𐐒","C":"Ɔ","D":"◖","E":"Ǝ","F":"Ⅎ","G":"⅁","H":"H","I":"I","J":"ſ","K":"⋊",
            "L":"˥","M":"W","N":"N","O":"O","P":"Ԁ","Q":"Ό","R":"ᴚ","S":"S","T":"⊥","U":"∩","V":"Λ","W":"M","X":"X","Y":"⅄","Z":"Z",
            "1":"Ɩ","2":"ᄅ","3":"Ɛ","4":"ㄣ","5":"ϛ","6":"9","7":"ㄥ","8":"8","9":"6","0":"0",
            "?":"¿","!":"¡","(":")",")":"(","[":"]","]":"[","{":"}","}":"{","<":">",">":"<","'":",",",":"'","\"":"„"," ":" "
        },
        monospace: "𝚊𝚋𝚌𝚍𝚎𝚏𝚐𝚑𝚒𝚓𝚔𝚕𝚖𝚗𝚘𝚙𝚚𝚛𝚜𝚝𝚞𝚟𝚠𝚡𝚢𝚣𝙰𝙱𝙲𝙳𝙴𝙵𝙶𝙷𝙸𝙹𝙺𝙻𝙼𝙽𝙾𝙿𝚀𝚁𝚂𝚃𝚄𝚅𝚆𝚇𝚈𝚉𝟶𝟷𝟸𝟹𝟺𝟻𝟼𝟽𝟾𝟿"
    };

    // 2. Selección de elementos del DOM
    const select = (id) => ({
        input: document.querySelector(`[aria-describedby="${id}"]`),
        btn: document.getElementById(id)
    });

    const base = document.getElementById('texto-base');
    const counter = document.getElementById('char-counter');
    const fields = {
        negrita: select('button-negrita'),
        cursiva: select('button-cursiva'),
        negritaCursiva: select('button-negrita-cursiva'),
        tachado: select('button-tachado'),
        subrayado: select('button-subrayado'),
        subrayadoNegrita: select('button-subrayado-negrita'),
        invertido: select('button-invertido'),
        monospace: select('button-monospace')
    };


    // 3. Función de transformación
    const helpers = {
        // Función para limpiar acentos y eñes completamente y homogeneizar textos
        limpiar: (texto) => {
            return texto.normalize("NFD").replace(/[\u0300-\u036f]/g, "")
                        .replace(/ñ/g, "n").replace(/Ñ/g, "N");
        }
    };

    const transformadores = {
        // Usamos Array.from() para manejar correctamente los caracteres Unicode de 32 bits
        mapeo: (texto, tipo) => {
            const origen = alfabetos.normal;
            const destino = Array.from(alfabetos[tipo]);
            const debeNormalizar = document.getElementById('switch-normalizar').checked;

            // Si el usuario activó el switch, limpiamos el texto antes de empezar
            const textoAProcesar = debeNormalizar ? helpers.limpiar(texto) : texto;

            return Array.from(textoAProcesar).map(char => {
                const i = origen.indexOf(char);
                // Si el carácter está en nuestro alfabeto (A-Z, a-z), lo transformamos.
                // Si no está (como una 'ó' o 'ñ' sin normalizar), lo devolvemos tal cual.
                return i !== -1 ? destino[i] : char;
            }).join('');
        },
        tachado: (texto) => {
            // Usamos el carácter \u0336 (Long Stroke Overlay)
            // Aplicamos normalize para ayudar al renderizado
            return texto.split('').map(char => char + '\u0334').join('').normalize('NFC');
        },
        negritaSubrayado: (texto) => {
        const textoNegrita = transformadores.mapeo(texto, 'negrita');
        // Definimos las letras que tienen descendentes (en su versión normal)
        const conDescendentes = "gjpyqgGJPYQ"; 
        // const normal = alfabetos.normal;

        return Array.from(textoNegrita).map((char, index) => {
            // Buscamos la letra original correspondiente para saber si tiene descendente
            const letraOriginal = texto[index]; 
            
            if (char === ' ' || conDescendentes.includes(letraOriginal)) {
                return char; // Si tiene "cola", devolvemos la letra sin subrayado
            }
            return char + '\u0332'; // Para las demás, aplicamos el subrayado
        }).join('');
        },
        subrayado: (texto) => {
            const conDescendentes = "gjpyqgGJPYQ";
            return texto.split('').map(char => {
                if (char === ' ' || conDescendentes.includes(char)) {
                    return char;
                }
                return char + '\u0332';
            }).join('');
        },
        // Para Monospaciado: Mejor normalizar para evitar que se rompa la rejilla
        monospace: (texto) => {
            const limpio = helpers.normalizar(texto);
            const origen = alfabetos.normal;
            const destino = Array.from(alfabetos.monospace);
            
            return Array.from(limpio).map(char => {
                const i = origen.indexOf(char);
                return i !== -1 ? destino[i] : char;
            }).join('');
        },
        // Motor para el texto Invertido
        voltear: (texto) => {
            const debeNormalizar = document.getElementById('switch-normalizar').checked;
            const textoAProcesar = debeNormalizar ? helpers.limpiar(texto) : texto;
            
            // const origen = alfabetos.normal;
            // const destino = Array.from(alfabetos.invertido);

            // En el invertido: primero mapeamos y luego giramos el array
            return Array.from(textoAProcesar)
                .map(char => alfabetos.invertido[char] || char)
                .reverse()
                .join('');
        }
    };

    // 4. Evento de escucha (Real-time)
    const procesarTexto = () => {
        const val = base.value;
        const len = val.length;

        // --- Actualizar contadores ---
        counter.innerText = `${len} / 150`;
        counter.className = len > 120 ? 'badge bg-danger' : (len > 120 ? 'badge bg-warning text-dark' : 'badge bg-primary');

        // counterAuthor.innerText = `${len} / 3000`;
        // counterAuthor.className = len > 2500 ? 'badge bg-danger' : (len > 2000 ? 'badge bg-warning text-dark' : 'badge bg-primary');

        // Asignar inputs
        fields.negrita.input.value = transformadores.mapeo(val, 'negrita');
        fields.cursiva.input.value = transformadores.mapeo(val, 'cursiva');
        fields.negritaCursiva.input.value = transformadores.mapeo(val, 'negritaCursiva');
        
        // Tachado (U+0336) y Subrayado (U+0332)
        fields.tachado.input.value = transformadores.tachado(val, '\u0336');
        fields.subrayado.input.value = transformadores.subrayado(val, '\u0332');
        fields.subrayadoNegrita.input.value = transformadores.negritaSubrayado(val);
        
        fields.invertido.input.value = transformadores.voltear(val);
        fields.monospace.input.value = transformadores.mapeo(val, 'monospace');
    };

        // Tu evento original (se queda igual de funcional)
        base.addEventListener('input', procesarTexto);

        // El nuevo evento para el switch (llama a la misma lógica)
        document.getElementById('switch-normalizar').addEventListener('change', procesarTexto);

    // 5. Función para copiar al portapapeles
    const configurarBoton = (field) => {
        field.btn.addEventListener('click', async () => {
            if (!field.input.value) return;
            try {
                await navigator.clipboard.writeText(field.input.value);
                const originalText = field.btn.innerHTML;
                field.btn.innerText = "¡Copiado!";
                field.btn.classList.replace('btn-outline-secondary', 'btn-success');
                setTimeout(() => {
                    field.btn.innerHTML = originalText;
                    field.btn.classList.replace('btn-success', 'btn-outline-secondary');
                }, 1000);
            } catch (err) {
                console.error("Error al copiar", err);
            }
        });
    };
    // Inicializar todos los botones
    Object.values(fields).forEach(configurarBoton);
});

/* Modo noche dia*/ 

document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    const htmlElement = document.documentElement;
    
    // 1. Inicializar el Tooltip de Bootstrap
    const tooltip = new bootstrap.Tooltip(themeToggle);

    const aplicarTema = (tema) => {
        htmlElement.setAttribute('data-bs-theme', tema);
        if (themeIcon) {
            const nuevoTexto = tema === 'dark' ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro';
            themeIcon.innerText = tema === 'dark' ? '☀️' : '🌙';
            // Actualizar el contenido del tooltip dinámicamente
        themeToggle.setAttribute('data-bs-original-title', nuevoTexto); 
        tooltip.setContent({ '.tooltip-inner': nuevoTexto });
        }
        localStorage.setItem('linkstyle-theme', tema);
        console.log("Tema aplicado:", tema); // Para depuración
    };

    // Al cargar la página
    const temaGuardado = localStorage.getItem('linkstyle-theme') || 
                         (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    
    aplicarTema(temaGuardado);

    // Evento de clic
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const temaActual = htmlElement.getAttribute('data-bs-theme');
            const nuevoTema = temaActual === 'dark' ? 'light' : 'dark';
            aplicarTema(nuevoTema);

        // Ocultar el tooltip al hacer click para que no se quede pegado
        tooltip.hide();
        });
    } else {
        console.error("No se encontró el botón con ID 'theme-toggle'");
    }
});