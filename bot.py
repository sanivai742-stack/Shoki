import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import requests

# আপনার টেলিগ্রাম বট টোকেন
BOT_TOKEN = "9122401277:AAES26isclACaL5Vuw_DaOc5s9iDcX2RU9Q"

# আপনার অন্যান্য কনফিগারেশন
ADMIN_ID = "7143948308"
API_KEY = "7e582ff9773fe5fd2c34777b03d800ccKk8U1aRzpiJNgtsjFeW5SbQwHd46VG0L"
BASE_API_URL = "https://shopvia1s.net/api"
GET_CODE_LINK = "https://mailgen.shop/get-inbox"

bot = telebot.TeleBot(BOT_TOKEN)

# মেইন মেনু কিবোর্ড
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton("🛒 Buy Now"), KeyboardButton("🔑 Mail Code"))
    markup.row(KeyboardButton("🔹 2FA Code"))
    markup.row(KeyboardButton("💵 Deposit"), KeyboardButton("🌐 Dashboard"))
    markup.row(KeyboardButton("😻 Support"))
    return markup

# /start কমান্ড
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🤖 **Secure Mail & IP Selling Bot**-এ আপনাকে স্বাগতম!\n\n"
        "নিচের বাটনগুলো থেকে আপনার প্রয়োজনীয় সেবাটি বেছে নিন:"
    )
    bot.send_message(message.chat.id, welcome_text, parse_mode="Markdown", reply_markup=main_menu())

# সব টেক্সট বাটন হ্যান্ডলার
@bot.message_handler(func=lambda message: True)
def handle_text_messages(message):
    text = message.text

    # ১. Buy Now (প্যাকেজ লিস্ট)
    if text == "🛒 Buy Now":
        inline_markup = InlineKeyboardMarkup(row_width=2)
        buttons = [
            InlineKeyboardButton("Ⓜ️ Hotmail", callback_data="cat_hotmail"),
            InlineKeyboardButton("Ⓜ️ Outlook", callback_data="cat_outlook"),
            InlineKeyboardButton("Ⓜ️ FR_Outlook", callback_data="cat_froutlook"),
            InlineKeyboardButton("🌐 VPN", callback_data="cat_vpn"),
            InlineKeyboardButton("Edu 💌 Mail", callback_data="cat_edumail"),
            InlineKeyboardButton("Proxy~IP", callback_data="cat_proxy"),
            InlineKeyboardButton("Ⓜ️ Gamil", callback_data="cat_gmail"),
            InlineKeyboardButton("🔡 Recovery Add mail", callback_data="cat_recovery"),
            InlineKeyboardButton("♾️ Meta Ai", callback_data="cat_meta"),
            InlineKeyboardButton("💟 NUMBER OTP", callback_data="cat_otp")
        ]
        inline_markup.add(*buttons)
        bot.send_message(message.chat.id, "✅ **প্যাকেজ সিলেক্ট করুন** 👇", parse_mode="Markdown", reply_markup=inline_markup)

    # ২. Mail Code
    elif text == "🔑 Mail Code":
        msg = (
            "✅ এখান থেকে মেইলের কোয়ালিটি চেক করতে পারবেন + bot মেইলের ওটিপি আসতে সময় লাগলে সাইট থেকে নিতে পারেন:\n\n"
            f"🔗 {GET_CODE_LINK}"
        )
        bot.send_message(message.chat.id, msg)

    # ৩. 2FA Code
    elif text == "🔹 2FA Code":
        bot.send_message(message.chat.id, "আপনার 2FA সিক্রেট কী (Secret Key) এখানে পাঠান, কোড জেনারেট করে দেওয়া হবে:")

    # ৪. Deposit (Binance & Manual)
    elif text == "💵 Deposit":
        deposit_markup = InlineKeyboardMarkup(row_width=1)
        deposit_markup.add(
            InlineKeyboardButton("🟡 Pay with Binance Pay", callback_data="pay_binance"),
            InlineKeyboardButton("📱 bKash / Nagad (Manual)", callback_data="pay_manual")
        )
        bot.send_message(
            message.chat.id, 
            "💳 **পেমেন্ট মেথড সিলেক্ট করুন:**", 
            parse_mode="Markdown",
            reply_markup=deposit_markup
        )

    # ৫. Dashboard
    elif text == "🌐 Dashboard":
        user_info = (
            f"👤 **আপনার ড্যাশবোর্ড**\n\n"
            f"🆔 ইউজার আইডি: `{message.from_user.id}`\n"
            f"👤 নাম: {message.from_user.first_name}\n"
            f"💰 একাউন্ট ব্যালেন্স: `0.00` টাকা"
        )
        bot.send_message(message.chat.id, user_info, parse_mode="Markdown")

    # ৬. Support
    elif text == "😻 Support":
        support_markup = InlineKeyboardMarkup()
        support_markup.add(InlineKeyboardButton("💬 Contact Admin", url=f"tg://user?id={ADMIN_ID}"))
        bot.send_message(
            message.chat.id, 
            f"যেকোনো প্রয়োজনে অ্যাডমিনের সাথে যোগাযোগ করুন।\nAdmin ID: `{ADMIN_ID}`", 
            parse_mode="Markdown",
            reply_markup=support_markup
        )

# ইনলাইন ক্যাটাগরি বাটন ক্লিক হ্যান্ডলার
@bot.callback_query_handler(func=lambda call: call.data.startswith("cat_"))
def handle_category_click(call):
    category = call.data.replace("cat_", "").upper()
    bot.answer_callback_query(call.id, f"{category} লোড হচ্ছে...")
    
    try:
        response = requests.get(f"{BASE_API_URL}/products.php?api_key={API_KEY}")
        if response.status_code == 200:
            bot.send_message(
                call.message.chat.id, 
                f"📦 **{category}** ক্যাটাগরির স্টক চেক সফল হয়েছে।\nকেনার জন্য এপিআই কানেক্টেড আছে।"
            )
        else:
            bot.send_message(call.message.chat.id, "⚠️ স্টক ডাটা লোড করতে সমস্যা হয়েছে।")
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Error: {str(e)}")

# পেমেন্ট অপশন হ্যান্ডলার
@bot.callback_query_handler(func=lambda call: call.data.startswith("pay_"))
def handle_payment_click(call):
    if call.data == "pay_binance":
        bot.answer_callback_query(call.id, "Binance Pay সিলেক্ট করা হয়েছে")
        binance_msg = (
            "🟡 **Binance Pay পেমেন্ট নির্দেশনা:**\n\n"
            "১. আমাদের বাইন্যান্স পে আইডি বা লিংকে পেমেন্ট পাঠান।\n"
            "📌 **Binance Pay ID:** `আপনার_বাইন্যান্স_আইডি_এখানে_দিন`\n\n"
            "২. টাকা পাঠিয়ে ট্রানজেকশন আইডি বা স্ক্রিনশট অ্যাডমিনকে দিন।\n"
            f"👤 অ্যাডমিন আইডি: `{ADMIN_ID}`"
        )
        bot.send_message(call.message.chat.id, binance_msg, parse_mode="Markdown")
        
    elif call.data == "pay_manual":
        bot.answer_callback_query(call.id, "বিকাশ/নগদ সিলেক্ট করা হয়েছে")
        bot.send_message(
            call.message.chat.id, 
            "📱 **বিকাশ / নগদ (Personal):** `01XXXXXXXXX`\n"
            "টাকা পাঠিয়ে ট্রানজেকশন আইডি (TrxID) দিন।"
        )

# বট রান করার কমান্ড (সঠিক নিয়ম)
if __name__ == "__main__":
    print("বট সফলভাবে চালু হয়েছে...")
    bot.infinity_polling()name__ == "__main__":
    print("বট সফলভাবে চালু হয়েছে...")
    bot.infinity_polling()lert=True)
        return
    await load_live(uid)
    cr = country_ranges(uid)
    if not cr:
        await c.message.edit_text(f"❌ {st['label']} এ এখন কোনো দেশের রেঞ্জ লাইভ নেই।",
                                  reply_markup=countries_kb({}))
        await c.answer()
        return
    await c.message.edit_text(countries_text(st["label"], cr), reply_markup=countries_kb(cr))
    await c.answer()


@dp.message(F.text == "☎️ GET NUMBER")
async def get_number(m: Message):
    await m.answer("📍 Select a service:", reply_markup=services_kb())


@dp.callback_query(F.data == "back")
async def back(c: CallbackQuery):
    await c.message.edit_text("📍 Select a service:", reply_markup=services_kb())
    await c.answer()


@dp.callback_query(F.data == "close")
async def close(c: CallbackQuery):
    uid = c.from_user.id
    if uid in polls:
        polls.pop(uid).cancel()
    try:
        await c.message.delete()
    except Exception:
        pass
    await c.answer()


@dp.callback_query(F.data.startswith("svc:"))
async def pick_service(c: CallbackQuery):
    j = int(c.data.split(":")[1])
    label, sid = SERVICE_MENU[j]
    st = state.setdefault(c.from_user.id, {})
    st["sid"], st["label"] = sid, label
    await show_countries(c)


@dp.callback_query(F.data == "chgc")
async def change_country(c: CallbackQuery):
    await show_countries(c)


@dp.callback_query(F.data.startswith("ct:"))
async def pick_country(c: CallbackQuery):
    st = state.setdefault(c.from_user.id, {})
    st["iso"] = c.data.split(":")[1]
    await allocate(c)


@dp.callback_query(F.data == "chg")
async def change_number(c: CallbackQuery):
    if "iso" not in (state.get(c.from_user.id) or {}):
        await c.answer("আবার GET NUMBER চাপুন", show_alert=True)
        return
    await allocate(c)


def number_kb(nums, otp=None):
    rows = []
    if otp:
        rows.append([InlineKeyboardButton(text=f"🔑 Copy OTP: {otp}", copy_text=CopyTextButton(text=str(otp)))])
    rows += [[InlineKeyboardButton(text=f"📋 +{n}", copy_text=CopyTextButton(text=f"+{n}"))] for n in nums]
    rows += [
        [InlineKeyboardButton(text="🔄 Change Number", callback_data="chg")],
        [InlineKeyboardButton(text="🌍 Change Country", callback_data="chgc")],
        [InlineKeyboardButton(text="🔔 Otp Group", url=OTP_GROUP_URL)],
    ]
    return InlineKeyboardMarkup(inline_keyboard=rows)


async def allocate(c: CallbackQuery):
    uid = c.from_user.id
    st = state[uid]
    iso = st["iso"]
    if uid in polls:
        polls.pop(uid).cancel()
    await c.answer("⏳ নাম্বার আনছি...")

    await load_live(uid)
    ranges = country_ranges(uid).get(iso, [])
    if not ranges:
        await c.message.answer("❌ এই দেশের রেঞ্জ এখন লাইভ নেই, অন্য দেশ বাছুন।")
        return

    nums, used, last_msg = [], [], ""
    attempts = 0
    while len(nums) < NUMBERS_PER_REQUEST and attempts < NUMBERS_PER_REQUEST + len(ranges) + 2:
        attempts += 1
        rng = random.choice(ranges)
        res = await np_call("getnum", {"range": rng, "requestId": secrets.token_hex(8)})
        meta = res.get("meta") or {}
        if meta.get("code") == 200 and res.get("data"):
            n = res["data"]["no_plus_number"]
            if n not in nums:
                nums.append(n)
                used.append(rng)
        else:
            last_msg = res.get("message") or "No number"
    if not nums:
        await c.message.answer(f"❌ নাম্বার পাওয়া যায়নি: {last_msg}")
        return

    head = (f"{_flag(iso)} {COUNTRIES[iso][1]} · {st['label']}\n"
            f"📡 Range: {', '.join(sorted(set(used)))}\n\n")
    msg = await c.message.edit_text(head + "⏳ Waiting for OTP...", reply_markup=number_kb(nums))
    polls[uid] = asyncio.create_task(poll_otp(uid, msg, head, nums))


async def poll_otp(uid: int, msg: Message, head: str, nums: list[str]):
    deadline = time.time() + POLL_TIMEOUT
    try:
        while time.time() < deadline:
            await asyncio.sleep(POLL_SECONDS)
            d = await np_call("inbox")
            for n in d.get("numbers") or []:
                if n.get("number") in nums and n.get("otp"):
                    await msg.edit_text(f"{head}✅ +{n['number']}\n🔑 OTP: <code>{n['otp']}</code>",
                                        parse_mode="HTML", reply_markup=number_kb(nums, otp=n["otp"]))
                    return
        await msg.edit_text(head + "⏰ OTP আসেনি। Change Number চাপুন।", reply_markup=number_kb(nums))
    except asyncio.CancelledError:
        pass
    except Exception as e:
        logging.error("poll error: %s", e)
    finally:
        if polls.get(uid) is asyncio.current_task():
            polls.pop(uid, None)


@dp.message(F.text == "📊 LIVE TRAFFIC")
async def live(m: Message):
    d = await np_call("liveaccess")
    services = (d.get("data") or {}).get("services") or []
    if not services:
        await m.answer("কোনো লাইভ ট্রাফিক নেই।")
        return
    lines = []
    for s in services:
        ago = int(time.time() - s["last_at"] / 1000)
        lines.append(f"• <b>{s['sid']}</b> — {len(s['ranges'])} ranges, last {ago // 60}m ago")
    await m.answer("📊 Live Traffic\n\n" + "\n".join(lines), parse_mode="HTML")


@dp.message(F.text == "💰 BALANCE")
async def balance(m: Message):
    await m.answer("💰 Balance: 0.00")  # ইউজার ব্যালেন্স সিস্টেম পরে যোগ হবে


@dp.message(F.text == "🟢 SUPPORT")
async def support(m: Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Contact", url=SUPPORT_URL)]])
    await m.answer("Support:", reply_markup=kb)


@dp.message(F.text == "⚙️ TOOLS")
async def tools(m: Message):
    await m.answer("⚙️ Tools coming soon")


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
