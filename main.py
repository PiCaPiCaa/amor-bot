import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TELEGRAM_TOKEN, ANABEL_ID, PICA_ID
import random

# Configuramos logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Frases muy románticas y variadas
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

# Comprobamos si el usuario es uno de los dos autorizados
def es_autorizado(user_id):
    return user_id == ANABEL_ID or user_id == PICA_ID

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not es_autorizado(update.effective_user.id):
        await update.message.reply_text("⛔ Este bot es privado solo para Anabel y PiCa.")
        return
    await update.message.reply_text(f"✨ Bienvenida mi niña preciosa ❤️\n\nHoy empieza nuestro rinconcito privado de amor 🌹")

# Comando /frase
async def frase(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not es_autorizado(update.effective_user.id):
        await update.message.reply_text("⛔ Este bot es privado.")
        return
    await update.message.reply_text(random.choice(frases))
# Comando /amor: mensajes súper románticos y personalizados
mensajes_amor = [
    "💘 Mi niña preciosa, aunque estemos separados por kilómetros, siento tu amor en cada latido.",
    "🌹 Anabel, eres el sueño que nunca quiero dejar de soñar.",
    "💫 PiCa te envía mil besos y abrazos a Sevilla desde Las Palmas.",
    "💕 Cada día que pasa, te quiero más, aunque solo te escriba por aquí.",
    "🌟 Contar los días para abrazarte es mi nueva obsesión hermosa.",
    "💖 No importa la distancia, porque mi corazón siempre te acompaña.",
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

async def amor(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not es_autorizado(update.effective_user.id):
        await update.message.reply_text("⛔ Este bot es solo para nosotros.")
        return
    await update.message.reply_text(random.choice(mensajes_amor))

# Comando /fecha: recuerda el día que empezasteis (7 de diciembre)
async def fecha(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not es_autorizado(update.effective_user.id):
        await update.message.reply_text("⛔ No autorizado.")
        return
    await update.message.reply_text("📅 Nuestro amor empezó el 7 de diciembre. Un día que nunca olvidaré ❤️")

# Comando /ayuda: muestra los comandos disponibles
async def ayuda(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not es_autorizado(update.effective_user.id):
        await update.message.reply_text("⛔ No autorizado.")
        return
    texto = (
        "🌹 Comandos disponibles:\n"
        "/start - Empezar con amor 💖\n"
        "/frase - Frase romántica para ti 🌸\n"
        "/amor - Mensaje de amor especial 💘\n"
        "/fecha - Recuerda nuestro día especial 📅\n"
        "/ayuda - Mostrar esta ayuda 😊"
    )
    await update.message.reply_text(texto)
# Función principal para arrancar el bot
async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("frase", frase))
    app.add_handler(CommandHandler("amor", amor))
    app.add_handler(CommandHandler("fecha", fecha))
    app.add_handler(CommandHandler("ayuda", ayuda))

    print("🤖 Bot arrancado y listo para dar amor ❤️")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())


