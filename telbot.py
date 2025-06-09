from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters
from telegram.error import BadRequest
import random
import time
import re
import asyncio

BOT_TOKEN = '8031927315:AAFTA3Uvs8rIUSxjqJUM8SY9CvF6K4zOb6E'
ADMIN_ID = 7978045298  # Ensure this is an int

# Sticker IDs (replace with your actual sticker file_ids)
STICKERS = {
    "welcome": "CAACAgUAAxkBAAEL3Npl6QABBY3sAAE1jQABLQABv4N4tJUUvAACBAACw7hIVQ8Z8VszJQABgjQE",
    "payment": "CAACAgUAAxkBAAEL3Nxl6QABBY3sAAE1jQABLQABv4N4tJUUvAACBAACw7hIVQ8Z8VszJQABgjQE",
    "verified": "CAACAgUAAxkBAAEL3N5l6QABBY3sAAE1jQABLQABv4N4tJUUvAACBAACw7hIVQ8Z8VszJQABgjQE",
    "error": "CAACAgUAAxkBAAEL3OBl6QABBY3sAAE1jQABLQABv4N4tJUUvAACBAACw7hIVQ8Z8VszJQABgjQE",
    "download": "CAACAgUAAxkBAAEL3OJl6QABBY3sAAE1jQABLQABv4N4tJUUvAACBAACw7hIVQ8Z8VszJQABgjQE"
}

APK_STORE = {
    "YouTube Premium with MicroG Settings": {
        "price": "₹10",
        "payment_link": "https://razorpay.me/@1mblogger?amount=CeQsAR0nTC%2BND0Le6liYzQ%3D%3D",
        "download_link": "https://drive.google.com/file/d/1H6r8PLTuZomutI6DTb1fYlkdmg4QAgev/view?usp=drive_link"
    },
    "KuKu FM Premium": {
        "price": "₹10",
        "payment_link": "https://razorpay.me/@1mblogger?amount=CeQsAR0nTC%2BND0Le6liYzQ%3D%3D",
        "download_link": "https://drive.google.com/file/d/1WbQM2R_j506lOiwFTnu0Ug7ftFouenh6/view?usp=drive_link"
    },
    "Call SMS Bomber": {
        "price": "₹5",
        "payment_link": "https://razorpay.me/@1mblogger?amount=CeQsAR0nTC%2BND0Le6liYzQ%3D%3D",
        "download_link": "https://yourhost.com/bomber.apk"
    },
    "DooFlix Premium": {
        "price": "₹10",
        "payment_link": "https://razorpay.me/@1mblogger?amount=CeQsAR0nTC%2BND0Le6liYzQ%3D%3D",
        "download_link": "https://yourhost.com/dooflix.apk"
    },
    "PicsArt Premium": {
        "price": "₹10",
        "payment_link": "https://razorpay.me/@1mblogger?amount=CeQsAR0nTC%2BND0Le6liYzQ%3D%3D",
        "download_link": "https://yourhost.com/picsart.apk"
    },
    "YouTube Music Premium": {
        "price": "₹10",
        "payment_link": "https://razorpay.me/@1mblogger?amount=CeQsAR0nTC%2BND0Le6liYzQ%3D%3D",
        "download_link": "https://yourhost.com/youtube-music.apk"
    },
    "TeraBox Premium": {
        "price": "₹10",
        "payment_link": "https://razorpay.me/@1mblogger?amount=CeQsAR0nTC%2BND0Le6liYzQ%3D%3D",
        "download_link": "https://drive.google.com/file/d/1WT8oHB16hyxWZ6ZfWgWvpEpw-otyNZNP/view?usp=drive_link"
    },
    "MX Player Pro Premium": {
        "price": "₹10",
        "payment_link": "https://razorpay.me/@1mblogger?amount=CeQsAR0nTC%2BND0Le6liYzQ%3D%3D",
        "download_link": "https://yourhost.com/mxplayer.apk"
    },
    "Jio HotStar Premium": {
        "price": "₹10",
        "payment_link": "https://razorpay.me/@1mblogger?amount=CeQsAR0nTC%2BND0Le6liYzQ%3D%3D",
        "download_link": "https://yourhost.com/hotstar.apk"
    },
    "Truecaller Premium": {
        "price": "₹10",
        "payment_link": "https://razorpay.me/@1mblogger?amount=CeQsAR0nTC%2BND0Le6liYzQ%3D%3D",
        # "download_link": "https://drive.google.com/file/d/1lCcb4pgs-C-8qA7YNFwSMY5TTsd4grWy/view?usp=drive_link"
        "download_link": "https://indianshortner.in/0IByGs"
    },
    "Spotify Premium": {
        "price": "₹10",
        "payment_link": "https://razorpay.me/@1mblogger?amount=CeQsAR0nTC%2BND0Le6liYzQ%3D%3D",
        "download_link": "https://drive.google.com/file/d/1UkOiEAAq7GbKDe7S9Hb5fLIuZinyNGYA/view?usp=drive_link"
    },
    "Panda VPN Premium": {
        "price": "₹10",
        "payment_link": "https://razorpay.me/@1mblogger?amount=CeQsAR0nTC%2BND0Le6liYzQ%3D%3D",
        "download_link": "https://drive.google.com/file/d/138OrNZkLPHxabv1tc2LAd2TGaqhlZ8Hm/view?usp=drive_link"
    },
    "ShotCut Premium": {
        "price": "₹10",
        "payment_link": "https://razorpay.me/@1mblogger?amount=CeQsAR0nTC%2BND0Le6liYzQ%3D%3D",
        "download_link": "https://drive.google.com/file/d/1WgqpK0q1ODZuOeL4Vq9ekLa9IVAvkQGJ/view?usp=drive_link"
    },
    "CapCut Premium": {
        "price": "₹10",
        "payment_link": "https://razorpay.me/@1mblogger?amount=CeQsAR0nTC%2BND0Le6liYzQ%3D%3D",
        "download_link": "https://drive.google.com/file/d/19aFT5FAg-yHHwN3snyohNQJra3G0-oCt/view?usp=drive_link"
    }
}

user_data = {}
download_links = {}  # Store download links and their status

async def send_with_sticker(context, chat_id, text, sticker_type):
    try:
        await context.bot.send_sticker(chat_id=chat_id, sticker=STICKERS[sticker_type])
    except:
        pass
    await context.bot.send_message(chat_id=chat_id, text=text, parse_mode='Markdown')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = """
✨ *Welcome to Premium APK Store!* ✨

Here you can get premium apps at unbelievable prices! 

🔹 *100% Working Mods*
🔹 *Instant Delivery*
🔹 *Trusted by Thousands*

👇 *Select the Premium APK you want:* 👇
    """
    
    keyboard = [[InlineKeyboardButton(apk, callback_data=apk)] for apk in APK_STORE]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    try:
        await context.bot.send_sticker(chat_id=update.message.chat_id, sticker=STICKERS["welcome"])
    except:
        pass
    
    await update.message.reply_text(
        welcome_msg, 
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def handle_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    apk_name = query.data
    apk_info = APK_STORE[apk_name]
    
    verification_code = f"APK{random.randint(1000, 9999)}"
    user_data[query.from_user.id] = {
        "selected_apk": apk_name,
        "verification_code": verification_code,
        "payment_done": False
    }

    message = f"""
🎁 *{apk_name}* 🎁
💵 *Price:* {apk_info['price']}

🔐 *VERIFICATION CODE:* `{verification_code}`
❗ *IMPORTANT:* You MUST include this code in payment notes/description

💳 *Payment Link:*
{apk_info['payment_link']}

📤 After payment, please send:
1. UTR/Transaction Number
2. Payment Screenshot

We'll verify manually and send your download link within minutes!
    """
    
    try:
        await context.bot.send_sticker(chat_id=query.from_user.id, sticker=STICKERS["payment"])
    except:
        pass
    
    await query.edit_message_text(message, parse_mode='Markdown')

async def handle_payment_proof(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id not in user_data:
        await send_with_sticker(
            context,
            update.message.chat_id,
            "⚠️ *Please select an APK first using /start*",
            "error"
        )
        return

    if user_data[user_id]["payment_done"]:
        await send_with_sticker(
            context,
            update.message.chat_id,
            "✅ *Your payment is already verified!*\nCheck your messages for the download link.",
            "verified"
        )
        return

    try:
        if update.message.photo:
            await context.bot.forward_message(
                chat_id=ADMIN_ID,
                from_chat_id=update.message.chat_id,
                message_id=update.message.message_id
            )
        elif update.message.text:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=f"📩 *New Payment Verification Request*\n\n"
                     f"👤 User: {user_id}\n"
                     f"📱 APK: {user_data[user_id]['selected_apk']}\n"
                     f"🔢 Verification Code: {user_data[user_id]['verification_code']}\n"
                     f"💳 UTR: {update.message.text}",
                parse_mode='Markdown'
            )
        
        confirmation_msg = """
✅ *Payment Proof Received!*

We've submitted your payment for verification. 
Our team will check it manually (usually within 5-10 minutes).

⌛ *Please wait patiently...*
You'll receive another message with your download link soon!
        """
        
        await send_with_sticker(
            context,
            update.message.chat_id,
            confirmation_msg,
            "payment"
        )
    except BadRequest as e:
        print(f"Failed to send message to admin: {e}")
        await send_with_sticker(
            context,
            update.message.chat_id,
            "⚠️ *Error processing your payment proof. Please try again later.*",
            "error"
        )

async def verify_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id != ADMIN_ID:
        return

    try:
        if not context.args or not context.args[0].isdigit():
            await update.message.reply_text("❌ Usage: /verify USER_ID", parse_mode=None)
            return

        user_id = int(context.args[0])

        if user_id in user_data:
            if not user_data[user_id]["payment_done"]:
                user_data[user_id]["payment_done"] = True
                apk_name = user_data[user_id]["selected_apk"]
                download_link = APK_STORE[apk_name]["download_link"]

                # Generate a unique key for this download
                download_key = f"DL{random.randint(1000, 9999)}_{int(time.time())}"
                download_links[download_key] = {
                    "user_id": user_id,
                    "apk_name": apk_name,
                    "link": download_link,
                    "used": False,
                    "created_at": time.time()
                }

                success_msg = f"""
🎉 Payment Verified! 🎉

📦 Product: {apk_name}
🔗 Download Link: /download_{download_key}

⚠️ WARNING: 
❗ This link will work only once!
❗ Click the button below to download immediately

📌 Instructions:
1. Click the download button below
2. You'll be redirected to download page
3. Install the APK
4. Enjoy premium features!
                """
                
                # Create inline keyboard with download button
                keyboard = [[
                    InlineKeyboardButton(
                        "⬇️ DOWNLOAD NOW ⬇️", 
                        callback_data=f"download_{download_key}"
                    )
                ]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                try:
                    sent_message = await context.bot.send_message(
                        chat_id=user_id,
                        text=success_msg,
                        reply_markup=reply_markup,
                        parse_mode=None
                    )
                    
                    # Store message info
                    user_data[user_id]["download_msg_id"] = sent_message.message_id
                    user_data[user_id]["download_key"] = download_key
                    
                    try:
                        await context.bot.send_sticker(
                            chat_id=user_id,
                            sticker=STICKERS["download"]
                        )
                    except:
                        pass
                    
                    await update.message.reply_text(
                        f"✅ Payment verified and link sent to user {user_id}\n"
                        f"📱 APK: {apk_name}\n"
                        f"🔢 Code: {user_data[user_id]['verification_code']}\n"
                        f"🔑 Download Key: {download_key}",
                        parse_mode=None
                    )
                except BadRequest as e:
                    if "blocked" in str(e).lower():
                        await update.message.reply_text(f"⚠️ User {user_id} has blocked the bot")
                    else:
                        await update.message.reply_text(f"⚠️ Failed to message user {user_id}: {e}")
            else:
                await update.message.reply_text(f"ℹ️ User {user_id}'s payment is already verified.")
        else:
            await update.message.reply_text("❌ No pending payment for this user.", parse_mode=None)
    except Exception as e:
        print(f"Error in verify_payment: {e}")
        await update.message.reply_text(f"⚠️ Error: {str(e)}")
        try:
            await context.bot.send_sticker(
                chat_id=update.message.chat_id,
                sticker=STICKERS["error"]
            )
        except:
            pass

async def handle_download_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Extract download key from callback data
    download_key = query.data.replace("download_", "")
    
    if download_key not in download_links:
        await query.edit_message_text("❌ Invalid download link or link has expired.")
        return
        
    link_data = download_links[download_key]
    
    # Check if link is expired (24 hours)
    if time.time() - link_data["created_at"] > 86400:
        await query.edit_message_text("⚠️ This download link has expired.")
        return
        
    if link_data["used"]:
        await query.edit_message_text("⚠️ This download link has already been used.")
        return
        
    if query.from_user.id != link_data["user_id"]:
        await query.edit_message_text("❌ This download link is not for you.")
        return
        
    # Mark link as used IMMEDIATELY
    download_links[download_key]["used"] = True
    
    # Create new message with direct download link
    download_msg = f"""
⬇️ Download {link_data['apk_name']} by clicking the button below:

⚠️ NOTE: This link can only be used once.
"""
    
    # Create inline keyboard with download button
    keyboard = [[
        InlineKeyboardButton(
            "⬇️ DOWNLOAD NOW ⬇️", 
            url=link_data["link"]
        )
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    # Send the download message
    await query.edit_message_text(
        text=download_msg,
        reply_markup=reply_markup
    )
    
    # Delete the message after 5 seconds
    await asyncio.sleep(5)
    try:
        await context.bot.delete_message(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
        )
    except:
        pass
    
    # Send thank you message
    await send_with_sticker(
        context,
        query.from_user.id,
        "✅ Thank you for downloading! Remember to save the APK file.",
        "verified"
    )

async def handle_download_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        command = update.message.text
        match = re.match(r'^/download_(DL\d+_\d+)$', command)
        if not match:
            await update.message.reply_text("❌ Invalid download link format.")
            return
            
        download_key = match.group(1)
        if download_key not in download_links:
            await update.message.reply_text("❌ Invalid download link or link has expired.")
            return
            
        link_data = download_links[download_key]
        
        # Check if link is expired (24 hours)
        if time.time() - link_data["created_at"] > 86400:
            await update.message.reply_text("⚠️ This download link has expired.")
            return
            
        if link_data["used"]:
            await update.message.reply_text("⚠️ This download link has already been used.")
            return
            
        if update.message.from_user.id != link_data["user_id"]:
            await update.message.reply_text("❌ This download link is not for you.")
            return
            
        # Mark link as used IMMEDIATELY
        download_links[download_key]["used"] = True
        
        # Create inline keyboard with download button
        keyboard = [[
            InlineKeyboardButton(
                "⬇️ DOWNLOAD NOW ⬇️", 
                url=link_data["link"]
            )
        ]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Send message with download button
        download_msg = await update.message.reply_text(
            f"⬇️ Download {link_data['apk_name']} by clicking the button below:",
            reply_markup=reply_markup
        )
        
        # Delete the message after 5 seconds
        await asyncio.sleep(5)
        try:
            await context.bot.delete_message(
                chat_id=update.message.chat_id,
                message_id=download_msg.message_id
            )
        except:
            pass
            
        # Send thank you message
        await send_with_sticker(
            context,
            update.message.from_user.id,
            "✅ Thank you for downloading! Remember to save the APK file.",
            "verified"
        )
        
    except Exception as e:
        print(f"Error in handle_download: {e}")
        await update.message.reply_text("⚠️ Error processing your download request.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_selection))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_payment_proof))
    app.add_handler(MessageHandler(filters.PHOTO, handle_payment_proof))
    app.add_handler(CommandHandler("verify", verify_payment))
    app.add_handler(CallbackQueryHandler(handle_download_button, pattern=r'^download_'))
    app.add_handler(MessageHandler(filters.Regex(r'^/download_'), handle_download_command))
    
    print("🤖 Bot is running and ready to serve...")
    app.run_polling()

if __name__ == '__main__':
    main()