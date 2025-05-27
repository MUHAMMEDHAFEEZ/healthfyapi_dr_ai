from django.core.management.base import BaseCommand
from medical_tips.models import MedicalTip
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Populates the database with sample medical tips in Egyptian Arabic'

    def _create_tips(self):
        # List of sample medical tips in Egyptian Arabic with appropriate time and duration combinations
        tip_templates = [
            {
                "title": "اشرب مية كتير",
                "content": "لازم تشرب 8 كباية مية في اليوم عشان صحتك",
                "valid_times": ["الصبح", "الضهر", "بالليل", "كل يوم"],
                "valid_durations": ["على مدار اليوم"]
            },
            {
                "title": "الرياضة مهمة",
                "content": "لازم تتحرك وتعمل رياضة نص ساعة 5 مرات في الأسبوع",
                "valid_times": ["الصبح", "بعد الضهر"],
                "valid_durations": ["نص ساعة", "ساعة"]
            },
            {
                "title": "الأكل الصحي",
                "content": "كل خضار وفاكهة كتير واتجنب الأكل السريع",
                "valid_times": ["كل يوم"],
                "valid_durations": ["على مدار اليوم"]
            },
            {
                "title": "النوم المظبوط",
                "content": "نام 8 ساعات في اليوم عشان تصحى نشيط ومركز",
                "valid_times": ["بالليل"],
                "valid_durations": ["8 ساعات"]
            },
            {
                "title": "الصحة النفسية",
                "content": "خد وقت للراحة وابعد عن التوتر والقلق",
                "valid_times": ["كل يوم"],
                "valid_durations": ["ساعة", "ساعتين"]
            },
            {
                "title": "وضعية الجسم",
                "content": "خلي بالك من طريقة قعدتك وانت قاعد على المكتب",
                "valid_times": ["كل ساعة"],
                "valid_durations": ["دقيقتين", "5 دقايق"]
            },
            {
                "title": "العناية بالعين",
                "content": "كل 20 دقيقة بص على حاجة بعيدة لمدة 20 ثانية",
                "valid_times": ["كل 20 دقيقة"],
                "valid_durations": ["20 ثانية"]
            },
            {
                "title": "نظافة السنان",
                "content": "اغسل سنانك مرتين في اليوم واستخدم الخيط السني",
                "valid_times": ["الصبح", "بالليل"],
                "valid_durations": ["3 دقايق", "5 دقايق"]
            },
            {
                "title": "غسيل الإيدين",
                "content": "اغسل إيديك كويس بالصابون",
                "valid_times": ["قبل وبعد الأكل", "بعد الحمام"],
                "valid_durations": ["20 ثانية", "30 ثانية"]
            },
            {
                "title": "التعامل مع الضغط",
                "content": "خد نفس عميق وحاول تهدى لما تحس بالتوتر",
                "valid_times": ["وقت الضغط"],
                "valid_durations": ["دقيقة", "3 دقايق", "5 دقايق"]
            }
        ]

        benefit_variations = [
            "عشان صحتك",
            "هيخليك أحسن",
            "هيفرق معاك",
            "هيقويك",
            "حياتك هتتظبط",
            "هتحس بفرق"
        ]

        tips_created = 0
        batch_size = 1000

        while tips_created < 5000:  # Reduced number of tips to avoid too much redundancy
            batch_tips = []
            for _ in range(min(batch_size, 5000 - tips_created)):
                template = random.choice(tip_templates)
                time_var = random.choice(template['valid_times'])
                duration_var = random.choice(template['valid_durations'])
                benefit_var = random.choice(benefit_variations)

                # Create variations of the title and content in Egyptian Arabic
                title = f"{template['title']} {benefit_var}"
                
                # Create a more logical content structure based on the tip type
                if duration_var == "على مدار اليوم":
                    content = f"{template['content']}. اعمل كده {time_var} {benefit_var}."
                else:
                    content = f"{template['content']}. اعمل كده {time_var} لمدة {duration_var} و{benefit_var}."

                batch_tips.append(MedicalTip(
                    title=title,
                    content=content,
                    is_active=True
                ))

                tips_created += 1
                if tips_created % 1000 == 0:
                    self.stdout.write(f"تم إنشاء {tips_created} نصيحة...")

            MedicalTip.objects.bulk_create(batch_tips)

        return tips_created

    def handle(self, *args, **kwargs):
        # First, delete all existing tips
        MedicalTip.objects.all().delete()
        self.stdout.write('تم مسح كل النصائح القديمة...')
        
        self.stdout.write('جاري إنشاء النصائح الطبية الجديدة...')
        tips_count = self._create_tips()
        self.stdout.write(self.style.SUCCESS(f'تم إنشاء {tips_count} نصيحة طبية بنجاح!')) 