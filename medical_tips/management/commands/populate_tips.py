from django.core.management.base import BaseCommand
from medical_tips.models import MedicalTip
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Populates the database with sample medical tips in Egyptian Arabic'

    def _create_tips(self):
        # List of sample medical tips in Egyptian Arabic
        tip_templates = [
            {
                "title": "اشرب مية كتير",
                "content": "لازم تشرب 8 كباية مية في اليوم عشان صحتك"
            },
            {
                "title": "الرياضة مهمة",
                "content": "لازم تتحرك وتعمل رياضة نص ساعة 5 مرات في الأسبوع"
            },
            {
                "title": "الأكل الصحي",
                "content": "كل خضار وفاكهة كتير واتجنب الأكل السريع"
            },
            {
                "title": "النوم المظبوط",
                "content": "نام 8 ساعات في اليوم عشان تصحى نشيط ومركز"
            },
            {
                "title": "الصحة النفسية",
                "content": "خد وقت للراحة وابعد عن التوتر والقلق"
            },
            {
                "title": "وضعية الجسم",
                "content": "خلي بالك من طريقة قعدتك وانت قاعد على المكتب"
            },
            {
                "title": "العناية بالعين",
                "content": "كل 20 دقيقة بص على حاجة بعيدة لمدة 20 ثانية"
            },
            {
                "title": "نظافة السنان",
                "content": "اغسل سنانك مرتين في اليوم واستخدم الخيط السني"
            },
            {
                "title": "غسيل الإيدين",
                "content": "اغسل إيديك كويس بالصابون لمدة 20 ثانية"
            },
            {
                "title": "التعامل مع الضغط",
                "content": "خد نفس عميق وحاول تهدى لما تحس بالتوتر"
            }
        ]

        # Variations to make tips more unique in Egyptian Arabic
        time_variations = ["الصبح", "الضهر", "بالليل", "كل يوم", "كل اسبوع", "كل شهر"]
        duration_variations = ["5 دقايق", "10 دقايق", "ربع ساعة", "نص ساعة", "ساعة"]
        benefit_variations = [
            "عشان صحتك",
            "هيخليك أحسن",
            "هيفرق معاك",
            "هيقويك",
            "حياتك هتتظبط",
            "هتحس بفرق"
        ]

        tips_created = 0
        batch_size = 1000  # Create tips in batches for better performance

        while tips_created < 10000:
            batch_tips = []
            for _ in range(min(batch_size, 10000 - tips_created)):
                template = random.choice(tip_templates)
                time_var = random.choice(time_variations)
                duration_var = random.choice(duration_variations)
                benefit_var = random.choice(benefit_variations)

                # Create variations of the title and content in Egyptian Arabic
                title = f"{template['title']} {benefit_var}"
                content = f"{template['content']}. جرب تعمل كده {time_var} لمدة {duration_var} و{benefit_var}."

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
        self.stdout.write('جاري إنشاء النصائح الطبية...')
        tips_count = self._create_tips()
        self.stdout.write(self.style.SUCCESS(f'تم إنشاء {tips_count} نصيحة طبية بنجاح!')) 