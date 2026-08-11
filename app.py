"""
تطبيق Flask لموقع تعريفي متعدّد الصفحات عن نظام Git.
كل مسار (route) يقابله صفحة حقيقية مستقلّة لها محتواها الخاص.
"""

from flask import Flask, render_template

app = Flask(__name__)


# ============================================================
#  بيانات الأخطاء الشائعة — مصدرٌ واحد للمحتوى (مبدأ DRY)
#  لإضافة خطأ جديد: أضِف قاموسًا هنا فقط، والقالب يعرضه تلقائيًّا.
# ============================================================
MISTAKES = [
    {
        "tag": "commit",
        "title": "كتبتُ رسالة Commit خاطئة",
        "problem": "حفظت لقطة برسالةٍ فيها خطأ إملائي أو وصفٍ غير دقيق، وتريد تصحيحها قبل رفعها.",
        "solution": "طالما لم ترفع اللقطة بعد، يمكنك تعديل رسالة آخر Commit مباشرةً دون إنشاء لقطةٍ جديدة.",
        "command": '<span class="cmt"># تعديل رسالة آخر لقطة</span>\n'
                   '<span class="kw">git</span> <span class="cmd">commit</span> <span class="arg">--amend -m "الرسالة الصحيحة"</span>',
    },
    {
        "tag": "staging",
        "title": "أضفتُ ملفًا بالخطأ إلى منطقة التجهيز",
        "problem": "نفّذت git add لملفٍ لم تكن تقصد تضمينه في اللقطة القادمة، وتريد إخراجه من التجهيز.",
        "solution": "أخرِج الملف من منطقة التجهيز دون أن تفقد أي تغييرٍ فيه؛ سيبقى محفوظًا في مجلّد العمل.",
        "command": '<span class="cmt"># إخراج ملف من منطقة التجهيز</span>\n'
                   '<span class="kw">git</span> <span class="cmd">restore</span> <span class="arg">--staged file.txt</span>',
    },
    {
        "tag": "branch",
        "title": "عملتُ على الفرع الخطأ",
        "problem": "بدأت تعديلاتك على الفرع الرئيسي (main) بينما كان يُفترض أن تكون على فرعٍ مستقل.",
        "solution": "أنشئ فرعًا جديدًا وانتقل إليه؛ ستنتقل تعديلاتك غير المحفوظة معك إليه بأمان.",
        "command": '<span class="cmt"># إنشاء فرع جديد ونقل عملك إليه</span>\n'
                   '<span class="kw">git</span> <span class="cmd">switch</span> <span class="arg">-c feature/my-work</span>',
    },
    {
        "tag": "conflict",
        "title": "واجهتُ تعارضًا عند الدمج (Merge Conflict)",
        "problem": "عند دمج فرعين عدّلا السطر نفسه، يتوقّف Git ويطلب منك اختيار النسخة الصحيحة يدويًّا.",
        "solution": "افتح الملف المتعارض، وستجد التغييرات محدّدة برموز خاصّة. احتفظ بما تريد، احذف الرموز، ثم احفظ لقطةً بالحلّ.",
        "command": '<span class="cmt"># بعد تعديل الملفات المتعارضة يدويًّا</span>\n'
                   '<span class="kw">git</span> <span class="cmd">add</span> <span class="arg">.</span>\n'
                   '<span class="kw">git</span> <span class="cmd">commit</span>',
    },
    {
        "tag": "undo",
        "title": "أريد التراجع عن آخر Commit",
        "problem": "حفظت لقطةً ثم أدركت أنك تريد التراجع عنها، مع الاحتفاظ بالتغييرات لمراجعتها من جديد.",
        "solution": "تراجَع عن اللقطة الأخيرة مع إبقاء تغييراتها في مجلّد العمل، فتعيد ترتيبها كما تشاء.",
        "command": '<span class="cmt"># التراجع عن آخر لقطة مع الاحتفاظ بالتغييرات</span>\n'
                   '<span class="kw">git</span> <span class="cmd">reset</span> <span class="arg">--soft HEAD~1</span>',
    },
]


# * الصفحة الرئيسية — القسم الافتتاحي
@app.route("/")
def index():
    return render_template("index.html", active="home")


# * صفحة التعريف — ما هو Git
@app.route("/what")
def what():
    return render_template("what.html", active="what")


# * صفحة الأهمية — لماذا Git مهم
@app.route("/why")
def why():
    return render_template("why.html", active="why")


# * صفحة المفاهيم الأساسية + مقارنة Git وGitHub
@app.route("/concepts")
def concepts():
    return render_template("concepts.html", active="concepts")


# * صفحة طرق الاستخدام وسير العمل
@app.route("/usecases")
def usecases():
    return render_template("usecases.html", active="usecases")


# * صفحة الأخطاء الشائعة — تقرأ محتواها من قائمة MISTAKES
@app.route("/mistakes")
def mistakes():
    return render_template("mistakes.html", active="mistakes", mistakes=MISTAKES)


# * صفحة الأسئلة الشائعة والدعوة للبدء
@app.route("/faq")
def faq():
    return render_template("faq.html", active="faq")


# ! معالج الخطأ 404 — يعرض صفحةً مخصّصة بدل رسالة Flask الافتراضية
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", active=None), 404


if __name__ == "__main__":
    # ! التشغيل في وضع التطوير — لا تستعمل debug=True في بيئة الإنتاج
    app.run(host="127.0.0.1", port=5000, debug=True)
