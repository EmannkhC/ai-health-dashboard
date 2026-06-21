
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="AI Impact on Health", page_icon="🩺", layout="wide")

st.title("🩺 AI Impact on Health Dashboard")
st.write("""
هذه الداشبورد التفاعلية تستعرض نتائج دراسة شملت 5000 مشارك حول تأثير استخدام
أدوات الذكاء الاصطناعي الصحية (مثل Fitness Tracker وMental Health App وTelemedicine
وDiagnostic Assistant) على المؤشرات الصحية للمستخدمين.

تقارن الداشبورد بين الحالة الصحية قبل وبعد استخدام هذه الأدوات، وتحلل العلاقة بين
عوامل مختلفة مثل العمر، مستوى النشاط الرياضي، وساعات الاستخدام الأسبوعية،
مع نسبة التحسن ومستوى رضا المستخدمين عن كل أداة.
""")
st.divider()

@st.cache_data
def load_data():
    df = pd.read_csv("AI_Impact_on_Health_Dataset_5000_Enhanced.csv")

    age_order = ["18-25", "26-35", "36-45", "46-55", "56-65", "66-79"]
    df["Age_Group"] = pd.Categorical(df["Age_Group"], categories=age_order, ordered=True)

    level_order = ["Low", "Medium", "High"]
    for col in ["AI_Usage_Level", "Satisfaction_Level", "Risk_Category"]:
        df[col] = pd.Categorical(df[col], categories=level_order, ordered=True)

    exercise_order = ["Sedentary", "Moderate", "Active"]
    df["Exercise_Level"] = pd.Categorical(df["Exercise_Level"], categories=exercise_order, ordered=True)

    improve_order = ["Declined", "No Change", "Improved", "Highly Improved"]
    df["Improvement_Category"] = pd.Categorical(df["Improvement_Category"], categories=improve_order, ordered=True)

    return df

df = load_data()
sns.set_style("whitegrid")

st.subheader("👥 توزيع الأعمار (Age Distribution of Participants)")
fig, ax = plt.subplots(figsize=(8, 5))
sns.histplot(df["Age"], bins=20, kde=True, color="#66c2a5", ax=ax)
ax.set_title("Age Distribution of Participants")
ax.set_xlabel("Age")
ax.set_ylabel("Number of Participants")
st.pyplot(fig)
st.info(
    f"متوسط العمر {df[\'Age\'].mean():.1f} سنة، والمدى من {df[\'Age\'].min()} إلى {df[\'Age\'].max()}. "
    "التوزيع متوازن نسبياً بين الفئات العمرية بدون تركّز واضح في فئة معينة."
)
st.divider()

st.subheader("⚙️ نسبة التحسن حسب مستوى استخدام الذكاء الاصطناعي (Improvement % by AI Usage Level)")
fig, ax = plt.subplots(figsize=(8, 5))
sns.boxplot(data=df, x="AI_Usage_Level", y="Improvement_Percentage", hue="AI_Usage_Level",
            palette="Set2", legend=False, ax=ax)
ax.set_title("Improvement % by AI Usage Level")
ax.set_xlabel("AI Usage Level")
ax.set_ylabel("Improvement %")
st.pyplot(fig)
usage_means = df.groupby("AI_Usage_Level", observed=True)["Improvement_Percentage"].mean()
st.info(
    f"الفروقات بسيطة جداً بين المستويات: Medium ({usage_means.get(\'Medium\', 0):.1f}%)، "
    f"High ({usage_means.get(\'High\', 0):.1f}%)، Low ({usage_means.get(\'Low\', 0):.1f}%). "
    "يعني كثرة الاستخدام ما ترفع نسبة التحسن بشكل ملحوظ."
)
st.divider()

st.subheader("🧠 متوسط نسبة التحسن حسب نوع أداة الذكاء الاصطناعي (Average Improvement % by AI Tool Type)")
order_tool = df.groupby("AI_Tool_Type", observed=True)["Improvement_Percentage"].mean().sort_values(ascending=False).index
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=df, x="AI_Tool_Type", y="Improvement_Percentage", hue="AI_Tool_Type",
            order=order_tool, palette="Set2", errorbar=None, legend=False, ax=ax)
ax.set_title("Average Improvement % by AI Tool Type")
ax.set_xlabel("AI Tool Type")
ax.set_ylabel("Average Improvement %")
plt.setp(ax.get_xticklabels(), rotation=15)
st.pyplot(fig)
tool_means = df.groupby("AI_Tool_Type", observed=True)["Improvement_Percentage"].mean().sort_values(ascending=False)
st.info(
    f"{tool_means.index[0]} في المقدمة ({tool_means.iloc[0]:.1f}%)، تليها أدوات متقاربة جداً "
    f"({tool_means.iloc[1]:.1f}% - {tool_means.iloc[2]:.1f}%)، و{tool_means.index[-1]} الأقل "
    f"({tool_means.iloc[-1]:.1f}%). الفروقات بين الأدوات الأربع صغيرة جداً."
)
st.divider()

st.subheader("😀 توزيع مستوى الرضا حسب نوع الأداة (Satisfaction Level Distribution by AI Tool Type)")
ct = pd.crosstab(df["AI_Tool_Type"], df["Satisfaction_Level"], normalize="index") * 100
fig, ax = plt.subplots(figsize=(9, 5))
ct.plot(kind="bar", stacked=True, colormap="coolwarm", ax=ax)
ax.set_title("Satisfaction Level Distribution by AI Tool Type")
ax.set_xlabel("AI Tool Type")
ax.set_ylabel("Percentage %")
plt.setp(ax.get_xticklabels(), rotation=15)
ax.legend(title="Satisfaction Level")
st.pyplot(fig)
st.info(
    "كل الأدوات متقاربة جداً في توزيع الرضا (حوالي 28-31% رضا عالٍ، 28-30% منخفض، و~40% متوسط لكل أداة). "
    "الرضا عن الأداة لا يرتبط بنوعها — يبدو إنه عامل شخصي أكثر من كونه خاصية بالأداة نفسها."
)
st.divider()

st.subheader("🏃 متوسط نسبة التحسن حسب مستوى النشاط الرياضي (Average Improvement % by Exercise Level)")
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(data=df, x="Exercise_Level", y="Improvement_Percentage", hue="Exercise_Level",
            palette="Set2", errorbar=None, legend=False, ax=ax)
ax.set_title("Average Improvement % by Exercise Level")
ax.set_xlabel("Exercise Level")
ax.set_ylabel("Average Improvement %")
st.pyplot(fig)
exercise_means = df.groupby("Exercise_Level", observed=True)["Improvement_Percentage"].mean()
st.info(
    f"نتيجة غير متوقعة: Sedentary سجلوا أعلى متوسط تحسن ({exercise_means.get(\'Sedentary\', 0):.1f}%)، "
    f"يليهم Active ({exercise_means.get(\'Active\', 0):.1f}%)، ثم Moderate ({exercise_means.get(\'Moderate\', 0):.1f}%). "
    "ما فيه علاقة منطقية تصاعدية بين النشاط الرياضي والتحسن في هذه البيانات."
)
st.divider()

st.subheader("📌 الخلاصة العامة")
st.warning(
    "النمط المتكرر في كل الرسومات أعلاه: الفروقات بين الفئات (نوع الأداة، مستوى الاستخدام، "
    "مستوى النشاط) صغيرة جداً وغير منطقية الاتجاه أحياناً (الأقل استخدام/نشاط يحصل نتيجة أفضل). "
    "هذا مؤشر قوي إن التحسن في البيانات عشوائي بطبيعته ومستقل عن باقي المتغيرات، "
    "أي أن البيانات على الأغلب Synthetic / مولّدة عشوائياً وليست واقعية تماماً."
)
