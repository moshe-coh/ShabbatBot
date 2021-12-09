from shabat import get_in, get_out, get_shabbat_info

parasha = get_shabbat_info()[0]
date = get_shabbat_info()[1]

knisat = f"""
ירושלים: {get_in(geotag=281184)}
תל אביב: {get_in(293397)}
חיפה: {get_in(geotag=294801)}
באר שבע: {get_in(geotag=295530)}
"""

tzet = f"""
ירושלים: {get_out(geotag=281184)}
תל אביב: {get_out(geotag=293397)}
חיפה: {get_out(geotag=294801)}
באר שבע: {get_out(geotag=295530)}
"""

zmanim = """
זמני כניסת ויציאת השבת ל**{}** שתחול בתאריך: **{}**

**זמני כניסת השבת:**
{}
**זמני יציאת השבת:**
{}

""".format(parasha, date, knisat, tzet)

good_shabat = "**שבת שלום לכל חברי הקבוצה! הקבוצה סגורה לשליחת הודעות.**"

good_week = "**שבוע טוב לכל חברי הקבוצה! הקבוצה פתוחה לכתיבת הודעות.**"

start_msg = "**היי {}**\n\n" \
            "ברוכים הבאים לרובוט היחיד בטלגרם שישמור את השבת בקבוצה שלך.\nשלח /help על מנת לדעת איך להשתמש בי"

HELP_MSG = [
    ".",

    "**שומר שבת 🕯**\n__הרובוט היחיד בטלגרם שישמור את השבת בקבוצה שלך\nעבור לעמוד הבא על מנת להבין איך להשתמש בי 🇮🇱__",

    "**הפעלה ⚜️**\nיש להוסיף אותי לקבוצה שלך כמנהל עם הרשאות לחסימת משתמשים ושינוי הרשאות.\n**לאחר ההוספה חובה לשלוח "
    "את הפקודה `/add` אחרת אני לא אשמור את השבת אצלך בקבוצה...**",

    "**פקודות 💡**\n/add - שליחת פקודה זו בקבוצה תוסיף את הקבוצה לבסיס נתונים על מנת שהיא תסגר בשבת!\n/shabat - הצגת "
    "זמני כניסת ויציאת השבת \n/remove - הסרת הקבוצה מהבסיס נתונים... הקבוצה לא תסגר בשבת!\n/settings - התאם אישית את "
    "הרובוט בקבוצה שלך. עבור לעמוד הבא להוראות השימוש בפקודה זו",
    "**מה אפשר לעשות בהגדרות ⚙️**\n\n באפשרוכתם להגדיר האם הקבוצה תקבל מידי יום שישי (בשעה 13:30) הודעה עם זמני כניסת השבת!\n"
    " כמו כן באפשרוכתם להגדיר הודעה מותאמת אישית שתשלח בערב שבת כשהקבוצה נסגרת.",

    "__אם עדיין לא הבנתם את ההוראות או שיש לכם שאלות נוספות אתם מוזמנים לשאול בקבוצת תמיכה.__\n\n**פותח על ידי - @JewishBots**"
]
