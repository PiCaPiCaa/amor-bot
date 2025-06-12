import logging
import asyncio
import nest_asyncio
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import random
import json
from datetime import datetime

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Variables de entorno
load_dotenv()
nest_asyncio.apply()

# Cargar token
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# Archivo de respuestas
RESPUESTAS_FILE = "respuestas.json"

# Cargar respuestas guardadas
if os.path.exists(RESPUESTAS_FILE):
    with open(RESPUESTAS_FILE, "r") as f:
        respuestas_guardadas = json.load(f)
else:
    respuestas_guardadas = {}

# Frases y mensajes de amor
frases = [
    "💖 Aunque estemos lejos, siempre estás muy cerca de mi corazón.",
    "🌹 Desde Las Palmas hasta Sevilla, mi amor por ti cruza cualquier distancia.",
    "✨ 7 de diciembre empezó lo más bonito que me ha pasado: tú.",
    "🌙 Cada noche me acuesto soñando con el día que por fin te vea en persona.",
    "💞 Eres mi niña, mi amor, mi ilusión, mi todo. Gracias por existir.",
    "🚀 Aunque nunca nos hayamos visto aún, siento que te conozco de alma a alma.",
    "💌 Este amor a distancia me enseña lo valiosa que eres para mí cada día.",
    "🌷 Pienso en ti cada mañana, cada tarde y cada noche. Siempre tú.",
    "💖 Mi niña bonita de Sevilla... qué ganas de tenerte entre mis brazos.",
    "🌟 Por muchos kilómetros que haya, mi corazón late solo por ti.",
    "💖 Aunque estemos lejos, siempre estás muy cerca de mi corazón.",
    "🌹 Desde Las Palmas hasta Sevilla, mi amor por ti cruza cualquier distancia.",
    "✨ 7 de diciembre empezó lo más bonito que me ha pasado: tú.",
    "🌙 Cada noche me acuesto soñando con el día que por fin te vea en persona.",
    "💞 Eres mi niña, mi amor, mi ilusión, mi todo. Gracias por existir.",
    "🚀 Aunque nunca nos hayamos visto aún, siento que te conozco de alma a alma.",
    "💌 Este amor a distancia me enseña lo valiosa que eres para mí cada día.",
    "🌷 Pienso en ti cada mañana, cada tarde y cada noche. Siempre tú.",
    "💖 Mi niña bonita de Sevilla... qué ganas de tenerte entre mis brazos.",
    "🌟 Por muchos kilómetros que haya, mi corazón late solo por ti.",
    "🌈 En la distancia, tu sonrisa es mi arcoíris favorito.",
    "💫 Nuestro amor es como las estrellas, infinito y brillante aunque lejos.",
    "🌻 Cada mensaje tuyo es un rayo de sol que ilumina mi día.",
    "❤️ Aunque no nos hayamos tocado, siento tu piel en mis pensamientos.",
    "🌺 La paciencia de esperar por ti es dulce porque sé que vales la pena.",
    "✨ En cada latido, un susurro: te amo, mi niña preciosa.",
    "🎶 Nuestra canción suena en mi cabeza desde que te conocí.",
    "🕊️ Eres mi paz en medio del caos, mi calma en la tormenta.",
    "💌 Guardaré cada palabra tuya como el tesoro más valioso.",
    "🌹 Aunque lejos, mi corazón siempre está contigo.",
    "🔥 Mi amor por ti arde más allá de cualquier distancia."
]

mensajes_amor = [
    "💘 Mi niña preciosa, aunque estemos separados por kilómetros, siento tu amor en cada latido.",
    "🌹 Anabel, eres el sueño que nunca quiero dejar de soñar.",
    "💫 PiCa te envía mil besos y abrazos a Sevilla desde Las Palmas.",
    "💕 Cada día que pasa, te quiero más, aunque solo te escriba por aquí.",
    "🌟 Contar los días para abrazarte es mi nueva obsesión hermosa.",
    "💖 No importa la distancia, porque mi corazón siempre te acompaña.",
    "🌹 Mi niña, mi amor, la luz que ilumina hasta mis días más grises.",
    "💞 Soñar contigo es mi refugio favorito, no quiero despertar jamás.",
    "🌷 Me enamoro de ti en cada palabra que compartimos.",
    "💌 No hay distancia que pueda con lo que siento por ti.",
    "✨ En el silencio de la noche, tu nombre es mi mantra sagrado.",
    "🔥 Mi corazón late fuerte solo por ti, mi amor imposible y perfecto.",
    "💫 Aunque no te haya visto, siento que te conozco mejor que nadie.",
    "🌈 Eres la melodía que llena mi vida de color y esperanza.",
    "💖 Gracias por enseñarme que el amor verdadero no tiene fronteras.",
    "🌟 Mi niña preciosa, no importa cuánto tiempo pase, siempre serás mi sueño.",
    "🌹 Guardaré nuestro amor como el secreto más bello de mi alma.",
    "💕 Te amo más allá de lo que las palabras pueden expresar.",
    "💞 Cada día contigo, aunque sea en mensajes, es un regalo del cielo.",
    "🔥 Eres la chispa que enciende mi alma y me hace querer ser mejor."
]

preguntas = [
    "💕 ¿Qué fue lo primero que pensaste cuando empezamos a hablar por chat?",
    "🔥 ¿Has imaginado alguna vez cómo sería nuestra primera noche juntos?",
    "😈 ¿Te gustaría que nos demos el primer beso lento o apasionado?",
    "🥰 ¿Qué parte de mi cuerpo crees que besarás primero?",
    "🎧 ¿Qué canción pondrías de fondo mientras hacemos el amor?",
    "🤤 ¿Qué ropa interior usarías para volverme loco la primera vez?",
    "💋 ¿Dónde te gustaría que te bese en público sin que nadie lo note?",
    "🌙 ¿En qué posición te gustaría dormir abrazados la primera vez?",
    "🌊 ¿Qué harías si estuviéramos juntos ahora mismo en una playa desierta?",
    "👀 ¿Has soñado con alguna escena íntima entre nosotros? ¿Cómo fue? 🔥",
    "🎁 ¿Qué sorpresa picante te gustaría que prepare la primera vez que nos veamos?",
    "🥵 ¿Te gusta hablar sucio? ¿Qué me dirías la primera vez en persona?",
    "🍑 ¿Qué zona de tu cuerpo es la más sensible al contacto? 😏",
    "🚿 ¿Haríamos juntos una ducha caliente y muy larga? ¿Cómo la imaginas? 💦",
    "🍷 ¿Prefieres una noche de pasión salvaje o caricias suaves y lentas? 😌",
    "📸 ¿Nos haríamos fotos íntimas privadas para recordar nuestra primera vez? 📷",
    "💄 ¿Te atreverías a usar un disfraz sexy para sorprenderme en privado? 🔥",
    "👄 ¿Cómo me besarías cuando estemos solos en casa? 💋",
    "💘 ¿Qué palabra secreta usaríamos para decirnos que queremos sexo sin que otros lo noten?",
    "🤫 ¿Tendrías sexo en un sitio público si supieras que nadie nos verá? 🙊",
    "💞 ¿Qué apodo hot me pondrías en la intimidad? 🔥",
    "👙 ¿Qué lencería me gustaría verte usar la primera noche? 😈",
    "🚪 ¿Cuál sería la primera habitación de la casa que usaríamos para estrenarla? 🏡",
    "🧳 ¿Qué llevarías en la maleta si supieras que vamos a pasar el primer fin de semana juntos? 🥵",
    "🤯 ¿Te atreverías a vendarme los ojos durante un juego íntimo? 🔗",
    "🎡 ¿Harías el amor en un sitio inesperado como un ascensor, cine o coche? 🚗",
    "🌅 ¿Qué harías si amanecemos desnudos abrazados después de nuestra primera noche?",
    "📱 ¿Has pensado enviarme alguna vez una foto muy picante? 📸",
    "🥂 ¿Brindarías conmigo desnudos después de hacer el amor? 🍾",
    "🔥 ¿Alguna vez tuviste una fantasía con alguien a quien no conocías físicamente?",
    "🍓 ¿Te gustaría que te dé de comer fruta en la cama mientras jugamos? 🍇",
    "🚫 ¿Hay algún límite o tabú que no cruzarías en la intimidad? 🚷",
    "😜 ¿Alguna vez te ha pasado tener sexo en un sitio donde podías ser descubierto? 👀",
    "💥 ¿Te gustaría probar juguetes íntimos en pareja? ¿Cuál primero? 🎮",
    "🛏️ ¿Prefieres sexo por la mañana, por la tarde o de madrugada? ⏰",
    "💨 ¿Qué movimiento crees que me volverá completamente loco en la cama? 🔥",
    "💡 ¿Has pensado en un juego de roles para sorprenderme? ¿Cuál sería? 🎭",
    "🍀 ¿Qué prenda mía te gustaría quedarte después de pasar la noche juntos? 👕",
    "🎶 ¿Qué canción sensual sería nuestro himno íntimo? 🎧",
    "🧡 ¿Harías un striptease para mí en la intimidad? 🔥",
    "🪞 ¿Te gustaría vernos en el espejo mientras estamos desnudos? 👀",
    "😈 ¿Has pensado alguna vez en un trío? ¿Con quién sería? 🔥",
    "🍫 ¿Usaríamos comida o chocolate en nuestros juegos íntimos? 🍯",
    "💎 ¿Qué joya íntima te pondrías solo para mí? 💍",
    "🌃 ¿Dormirías desnuda abrazada a mí después de hacer el amor? 🌙",
    "💌 ¿Qué mensaje hot me enviarías en plena madrugada si no pudiéramos vernos?",
    "🧨 ¿Qué es lo que más deseas hacerme la primera vez juntos? 🔥",
    "🌡️ ¿Te gustaría que tengamos una lista de posiciones por cumplir juntos? 📝",
    "🎙️ ¿Qué frase me dirías susurrando al oído mientras te acaricio?",
    "🍑 ¿Imaginas el sabor de mis besos? ¿Suaves o salvajes? 😘",
    "👅 ¿En qué parte de tu cuerpo quieres sentir primero mi lengua? 🔥",
    "🎁 ¿Qué sorpresa íntima te gustaría encontrar al llegar a mi habitación? 🛏️",
    "🤫 ¿Qué palabra mágica me dirías para empezar un juego prohibido? 🔐",
    "🩵 ¿Qué postura crees que nos hará perder el control la primera vez? 😏",
    "🍷 ¿Nos daríamos un baño de burbujas mientras nos acariciamos lentamente? 🛁",
    "💋 ¿Cómo te gustaría que te besara mientras te quito la ropa? 👗",
    "🎯 ¿Qué parte de mi cuerpo te obsesiona tocar cuando estemos juntos? 🔥",
    "🥵 ¿Te excita la idea de tener sexo después de mucho tiempo sin vernos? 🔥",
    "🚪 ¿Qué harías si al abrir la puerta me encuentras solo con una toalla? 😈",
    "🎬 ¿Te gustaría grabar nuestros momentos íntimos solo para nosotros? 🎥",
    "🍓 ¿Qué fruta usarías para jugar en la cama conmigo? 🍒",
    "🌙 ¿Nos gustaría dormir desnudos cada noche después de hacer el amor? 😴",
    "👄 ¿Dónde me besarías lentamente para provocarme aún más? 🔥",
    "🎲 ¿Inventarías un juego erótico solo para nuestras noches juntos? 🎮",
    "🌹 ¿Qué harías si me vieras salir de la ducha desnudo? 🚿",
    "🧴 ¿Usaríamos aceites calientes para masajes eróticos? 💦",
    "👀 ¿En qué lugar inesperado de la casa haríamos el amor? 🏠",
    "💞 ¿Te gustaría que tengamos palabras secretas para nuestras fantasías? 🔑",
    "🎭 ¿Qué disfraz erótico me pondrías en un juego de rol? 👮‍♂️👩‍⚕️",
    "🚨 ¿Tendrías sexo en un lugar donde puedan pillarnos? 👀",
    "💨 ¿Qué parte de tu cuerpo crees que besaré más tiempo? 😈",
    "👙 ¿Me harías un desfile privado de lencería? 🔥",
    "🖤 ¿Qué te excita más: la mirada, el tacto o las palabras? 🔥",
    "🍀 ¿Qué objeto sensual comprarías para usar juntos? 🛒",
    "👂 ¿Dónde me susurrarías tus deseos mientras te toco? 🎧",
    "🔥 ¿Qué sonido mío te excitaría más al hacer el amor? 🔊",
    "🎡 ¿Te atreverías a hacerlo en un sitio al aire libre? 🌳",
    "💋 ¿Cómo imaginas que serán mis caricias la primera vez? ✋",
    "🎯 ¿Qué fantasía aún no me contaste y sueñas probar conmigo? 🤐",
    "🍫 ¿Nos jugaríamos un reto erótico con comida y postres? 🍮",
    "🎙️ ¿Qué palabra mía te hará perder el control en la cama? 🔥",
    "👅 ¿Me dejarías atarte las manos y jugar al control? 🔗",
    "🚿 ¿Cómo imaginas una ducha caliente juntos después del sexo? 💦",
    "💥 ¿Prefieres maratón de sexo o pequeños momentos intensos durante el día? 🔥",
    "💎 ¿Qué joya íntima te gustaría ponerme como sorpresa? 💍",
    "🎞️ ¿Nos atreveríamos a grabar un video privado solo para nosotros? 🎥",
    "💣 ¿Qué fantasía no convencional te gustaría cumplir conmigo? 🎯",
    "🍑 ¿Te excita la idea de hacerlo en frente de un espejo? 🪞",
    "🍸 ¿Brindarías conmigo antes de nuestra primera vez? 🥂",
    "👀 ¿Qué mirada mía imaginas en el instante más caliente? 🔥",
    "🧨 ¿Harías el amor conmigo en la cocina? 🍳",
    "🛏️ ¿Qué posición sueñas probar primero conmigo? 📏",
    "🎯 ¿Qué te excitaría más: mis caricias suaves o mis mordiscos? 🧡",
    "🍯 ¿Probaríamos miel o nata para nuestros juegos? 🍦",
    "👀 ¿Qué zona de tu cuello es más sensible a mis besos? 🥰",
    "🔐 ¿Qué palabra secreta gritarías al llegar al orgasmo? 🔊",
    "🎁 ¿Me prepararías un striptease la primera noche? 💃",
    "💓 ¿Qué locura sexual siempre has querido probar y nunca te atreviste? 💥",
    "💦 ¿Haríamos el amor durante horas sin parar? 🛏️",
    "🎯 ¿Qué palabra sucia te gustaría que te diga mientras te acaricio? 🔥",
    "💋 ¿Te imaginas haciéndome un baile privado antes de la pasión? 💃",
    "😈 ¿Cuál sería el primer lugar salvaje donde lo haríamos cuando nos veamos? 🌍",
    "👄 ¿Dónde me besarías si solo pudieras elegir un sitio de mi cuerpo? 😘",
    "🍷 ¿Empezarías la primera noche con una copa de vino o directamente sin ropa? 🍾",
    "🌙 ¿Nos abrazaríamos desnudos toda la noche después de hacer el amor? 🌌",
    "💥 ¿Qué es lo más atrevido que te imaginas haciendo conmigo? 🔥",
    "👀 ¿Me mirarías fijamente mientras te quito lentamente la ropa? 😏",
    "🍫 ¿Nos embadurnamos de chocolate para un juego íntimo? 🍯",
    "🎮 ¿Haríamos un strip-póker solo los dos? ♠️",
    "🛁 ¿Te excita la idea de bañarnos desnudos en una bañera de espuma? 💦",
    "🍑 ¿Dónde me clavarías tus uñas cuando pierdas el control? 🔥",
    "🚪 ¿Me esperarías desnuda tras la puerta cuando llegue a verte? 😈",
    "🎯 ¿Qué parte de tu cuerpo quieres que explore con caricias infinitas? ✋",
    "💖 ¿Haríamos el amor mirando el amanecer juntos? 🌅",
    "🎬 ¿Nos grabaríamos jugando para vernos luego? 🎥",
    "😳 ¿Alguna vez has tenido sexo en un lugar público? ¿Dónde? 🚗",
    "💡 ¿Te gustaría hacerlo a oscuras o con una luz tenue viendo nuestros cuerpos? 🌙",
    "💥 ¿Prefieres movimientos rápidos o caricias largas y profundas? 😈",
    "💎 ¿Qué joya íntima llevarías escondida para sorprenderme? 💍",
    "🔥 ¿Te gusta que te den órdenes suaves en la intimidad? 🔐",
    "🎭 ¿Qué rol interpretarías en un juego sexual? 👮‍♂️👩‍⚕️",
    "👂 ¿Dónde es el punto exacto de tu cuerpo que más te excita al contacto? 🎯",
    "🥵 ¿Has tenido alguna fantasía conmigo mientras te tocabas? 😈",
    "🩸 ¿Probarías una noche con ataduras suaves o vendas en los ojos? 🔗",
    "🍸 ¿Brindarías por la mejor noche de nuestras vidas? 🥂",
    "🪞 ¿Te excita mirarte al espejo mientras hacemos el amor? 👀",
    "🎶 ¿Qué canción pondrías para acompañar nuestros gemidos? 🔊",
    "🔥 ¿Te gusta el sexo lento, salvaje o ambos según el momento? 💣",
    "👑 ¿Serías mi reina en nuestra primera noche juntos? 👸",
    "🍓 ¿Qué fruta sensual te daría en la boca mientras estamos desnudos? 🍇",
    "🧨 ¿Te atreverías a hacerlo en el balcón bajo la luna? 🌙",
    "📱 ¿Me enviarías un audio erótico antes de vernos? 🎧",
    "🛏️ ¿Qué juego previo te gustaría que hiciéramos durante horas? 🔥",
    "🎯 ¿Me permitirías explorar cada rincón de tu cuerpo lentamente? ✋",
    "💋 ¿Preferirías mimos largos o pasión directa la primera vez? 🔥",
    "🎁 ¿Me harías un regalo íntimo solo para usarlo en la cama? 🎀",
    "💦 ¿Te gusta gemir bajito o dejarte llevar sin control? 🔊",
    "🚗 ¿Te excitaría hacerlo en el coche bajo la lluvia? 🌧️",
    "🎯 ¿Qué rincón del hotel usaríamos primero? 🛏️",
    "🧸 ¿Haríamos cucharita desnudos después de amarnos? 🤗",
    "🎮 ¿Probaríamos un juego de retos calientes para romper el hielo? 🎲",
    "🕯️ ¿Encenderíamos velas alrededor de la cama? 🕯️",
    "👄 ¿Dejarías que recorra tu cuerpo solo con los labios? 🔥",
    "🚿 ¿Nos duchamos juntos después de cada encuentro? 💦",
    "🔥 ¿Harías que me vuelva adicto a tu cuerpo? 😈",
    "👀 ¿Te excita que te observe mientras llegas al clímax? 🔥",
    "🎭 ¿Harías un roleplay de enfermera, policía o profesora? 👩‍⚕️",
    "🎧 ¿Me susurrarías tus fantasías mientras estamos abrazados? 🥰",
    "🎯 ¿Me dejarías acariciarte lentamente mientras estás con los ojos vendados? 🔥",
    "🍑 ¿Qué parte de tu cuerpo quieres que recorra con mi lengua durante minutos? 😈",
    "🔥 ¿Te atreverías a hacerlo en plena madrugada mientras todos duermen? 🌙",
    "🎁 ¿Qué me regalarías después de una noche intensa de pasión? 🎀",
    "👀 ¿Te excita la idea de hacerlo en la terraza bajo las estrellas? 🌟",
    "💋 ¿Qué parte de mi cuerpo besarías primero al encontrarnos? 😘",
    "🍷 ¿Nos desnudaríamos lentamente con música sensual de fondo? 🎶",
    "💦 ¿Te gustaría experimentar sexo bajo la ducha con caricias interminables? 🚿",
    "👄 ¿Qué gemido mío te volvería loca mientras te hago el amor? 🔊",
    "🎮 ¿Harías un reto de preguntas calientes donde quien pierda, cumpla un deseo? 🎲",
    "🔥 ¿Te excita hablarme de tus fantasías cuando estás sola? 📱",
    "💎 ¿Qué joya íntima llevarías solo para provocarme en privado? 💍",
    "🚗 ¿Haríamos el amor en un mirador viendo las luces de la ciudad? 🌃",
    "🎯 ¿Qué rincón de tu cuerpo quieres que explore durante horas? ✋",
    "🍓 ¿Qué fruta morderías lentamente para provocarme? 🍒",
    "🛏️ ¿Haríamos el amor durante toda una noche sin dormir? 🌙",
    "🎧 ¿Me susurrarías lo que quieres que te haga mientras te acaricio? 🎙️",
    "💥 ¿Te excita que te domine suavemente en la intimidad? 🔐",
    "🚿 ¿Usaríamos aceites calientes para masajes sensuales interminables? 💦",
    "🔥 ¿Imaginas cómo será oler tu perfume en mi piel después de hacer el amor? 🥰",
    "👅 ¿Te gustaría que recorra cada centímetro de tu espalda desnuda con mis labios? 🔥",
    "🎭 ¿Qué fantasía secreta aún no me contaste? 🤫",
    "💋 ¿Dejarías que te bese el cuello hasta hacerte perder el control? 😘",
    "🧨 ¿Nos atreveríamos a cumplir una fantasía en un hotel de lujo? 🏨",
    "🎲 ¿Hacemos un juego donde cada prenda que quitamos es un reto cumplido? 🩲",
    "🍫 ¿Te gustaría probar juegos con comida y helado en la cama? 🍦",
    "🛁 ¿Haríamos el amor dentro de una bañera llena de espuma? 🫧",
    "👀 ¿Te excita la idea de hacerlo mientras solo nos miramos al espejo? 🪞",
    "💌 ¿Qué mensaje hot me escribirías justo antes de vernos? 🔥",
    "🎯 ¿Qué gritarías justo en el momento del clímax? 🔊",
    "💄 ¿Me dejarías desnudarte lentamente mientras te susurro al oído? 👗",
    "💥 ¿Qué movimiento mío haría que pierdas totalmente el control? 🔥",
    "👙 ¿Qué lencería usarías la primera noche para sorprenderme? 👙",
    "🧨 ¿Harías el amor en el balcón mientras vemos el amanecer? 🌅",
    "🔥 ¿Qué locura sexual harías si nadie nos viera jamás? 👀",
    "🍑 ¿Permitirías que recorra tu cuerpo mientras te digo lo que me enciende de ti? 🔥",
    "🎧 ¿Harías una playlist especial solo para nuestras noches? 🎶",
    "🛏️ ¿Te excita pensar en cuánto tiempo aguantaremos sin parar? 🔥",
    "👂 ¿Dónde me susurrarías un deseo secreto mientras te acaricio? 🎙️",
    "🍸 ¿Nos desnudaríamos lentamente después de un brindis privado? 🥂",
    "🎯 ¿Qué objeto te gustaría usar en nuestros juegos íntimos? 🔗",
    "🩷 ¿Te excita la idea de que te observe mientras te tocas? 👀",
    "🎁 ¿Qué sorpresa hot me prepararías tras nuestra primera cena juntos? 🍽️",
    "💦 ¿Haríamos maratones de caricias durante horas bajo las sábanas? 🛏️",
    "🌙 ¿Dormiríamos abrazados sin ropa cada noche? 🌌",
    "🔥 ¿Qué juego travieso me propondrías después de un baño juntos? 🚿",
    "💋 ¿Te gustaría susurrarme al oído mientras exploras mi cuerpo? 👄",
    "🎲 ¿Hacemos un juego de dados con pruebas eróticas? 🎲",
    "🧨 ¿Te excita que te susurre lo que quiero hacerte mientras te miro fijo? 👀",
    "💥 ¿Probaríamos juguetes eróticos para innovar juntos? 🎮",
    "🎭 ¿Inventarías una fantasía solo para sorprenderme cuando por fin nos veamos? 🔥"
]

pregunta_actual = {}

# Comandos

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✨ Bienvenida mi niña preciosa ❤️ Hoy empieza nuestro rinconcito privado de amor 🌹")

async def frase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(frases))

async def amor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(mensajes_amor))

async def fecha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📅 Nuestro amor empezó el 7 de diciembre. Un día que nunca olvidaré ❤️")

async def dias(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inicio = datetime(2023, 12, 7)
    hoy = datetime.now()
    dias_juntos = (hoy - inicio).days
    await update.message.reply_text(f"💖 Han pasado {dias_juntos} días desde que comenzó nuestra historia de amor. Cada día contigo es un regalo 🎁.")

async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    texto = (
        "🌹 Comandos disponibles:\n"
        "/start - Empezar 💖\n"
        "/frase - Frase romántica 🌸\n"
        "/amor - Mensaje de amor 💘\n"
        "/fecha - Fecha especial 📅\n"
        "/dias - Días juntos 📆\n"
        "/pregunta - Pregunta íntima 🔥\n"
        "/respuestas - Ver respuestas 📖\n"
        "/reset - Reiniciar tus respuestas 🔄\n"
        "/ayuda - Mostrar esta ayuda 😊\n"
               "Te Quiero Anabel💖 "
    )
    await update.message.reply_text(texto)

async def pregunta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    posibles = [p for p in preguntas if p not in respuestas_guardadas.get(user_id, {})]
    if not posibles:
        await update.message.reply_text("✅ Ya has respondido todas las preguntas.")
        return
    seleccionada = random.choice(posibles)
    pregunta_actual[user_id] = seleccionada
    await update.message.reply_text(f"❓ {seleccionada}")

async def manejar_respuesta(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id not in pregunta_actual:
        return
    respuesta = update.message.text
    pregunta = pregunta_actual[user_id]
    if user_id not in respuestas_guardadas:
        respuestas_guardadas[user_id] = {}
    respuestas_guardadas[user_id][pregunta] = respuesta
    with open(RESPUESTAS_FILE, "w") as f:
        json.dump(respuestas_guardadas, f, indent=4)
    await update.message.reply_text("💾 Respuesta guardada.")
    del pregunta_actual[user_id]

async def ver_respuestas(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id not in respuestas_guardadas or not respuestas_guardadas[user_id]:
        await update.message.reply_text("📭 Aún no has respondido ninguna pregunta.")
        return
    texto = "📖 Tus respuestas:\n"
    for pregunta, respuesta in respuestas_guardadas[user_id].items():
        texto += f"\n❓ {pregunta}\n💬 {respuesta}\n"
    await update.message.reply_text(texto)

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    if user_id in respuestas_guardadas:
        del respuestas_guardadas[user_id]
        with open(RESPUESTAS_FILE, "w") as f:
            json.dump(respuestas_guardadas, f, indent=4)
        await update.message.reply_text("🔄 Has reiniciado tus respuestas.")
    else:
        await update.message.reply_text("📭 No tienes respuestas guardadas aún.")

# Lanzar el bot
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("frase", frase))
    app.add_handler(CommandHandler("amor", amor))
    app.add_handler(CommandHandler("fecha", fecha))
    app.add_handler(CommandHandler("dias", dias))
    app.add_handler(CommandHandler("ayuda", ayuda))
    app.add_handler(CommandHandler("pregunta", pregunta))
    app.add_handler(CommandHandler("respuestas", ver_respuestas))
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), manejar_respuesta))

    print("🤖 Bot arrancado y listo para dar amor ❤️")
    await app.run_polling()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())

