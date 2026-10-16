import os, requests, feedparser, yfinance as yf

TOKEN = os.environ["TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]

STOCKS = ["AAPL","MSFT","NVDA","AMZN","GOOGL","META","TSLA","AMD","AVGO","NFLX"]
COMMODITIES = {"الذهب":"GC=F","النفط":"CL=F","الفضة":"SI=F","الغاز":"NG=F","النحاس":"HG=F"}
NEWS_SYMBOLS = ["^GSPC","GC=F","CL=F"]

def rsi(s, n=14):
    d = s.diff()
    up = d.clip(lower=0).rolling(n).mean()
    dn = (-d.clip(upper=0)).rolling(n).mean()
    return 100 - 100 / (1 + up / dn)

def scan(name, sym):
    df = yf.download(sym, period="1y", interval="1d", progress=False, auto_adjust=True)
    if df.empty or len(df) < 60:
        return None
    df.columns = df.columns.get_level_values(0)
    c, h, l, v = df["Close"], df["High"], df["Low"], df["Volume"]
    price = float(c.iloc[-1])
    breakout = price > float(h.iloc[-21:-1].max())
    trend = price > float(c.ewm(span=50).mean().iloc[-1])
    r = float(rsi(c).iloc[-1])
    avg_v = float(v.iloc[-21:-1].mean())
    vol_ok = avg_v > 0 and float(v.iloc[-1]) >= 1.2 * avg_v
    atr = float((h - l).rolling(14).mean().iloc[-1])
    if breakout and trend and 50 < r < 75 and vol_ok:
        sl = price - 1.5 * atr
        tp = price + 3 * atr
        return (f"📌 {name}\n🔹 دخول: {price:.2f}\n🛑 وقف: {sl:.2f}\n"
                f"🎯 هدف: {tp:.2f}\n📊 RSI: {r:.1f}")
    return None

def news():
    out = []
    for s in NEWS_SYMBOLS:
        url = f"https://feeds.finance.yahoo.com/rss/2.0/headline?s={s}&region=US&lang=en-US"
        for e in feedparser.parse(url).entries[:2]:
            out.append(f"• {e.title}\n{e.link}")
    return out

def main():
    trades = []
    for s in STOCKS:
        t = scan(s, s)
        if t: trades.append(t)
    for name, sym in COMMODITIES.items():
        t = scan(name, sym)
        if t: trades.append(t)

    msg = "🚀 تقرير السوق اليومي\n\n"
    msg += "\n\n".join(trades) if trades else "لا توجد فرص قوية اليوم."
    msg += "\n\n📰 أخبار:\n" + "\n".join(news())
    msg += "\n\n⚠️ للمعلومات فقط، وليست نصيحة استثمارية."

    requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage",
                  json={"chat_id": CHAT_ID, "text": msg[:4000]})

main()
