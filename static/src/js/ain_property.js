/** @odoo-module **/ 
import { _t } from "@web/core/l10n/translation";
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.Property = publicWidget.Widget.extend({
      selector: ".CompliantType",
      events: {
        "click #popup_button": "_onClickTogglePassword",
        "hidden.bs.modal #staticBackdrop": "_onCloseModal", // حدث إغلاق المودال
      },

    _onClickTogglePassword: function (ev) {
        // التقط الحدث
        const fileInput = document.getElementById('media_attachment'); // unchanged
        const mediaContainer = document.getElementById('media_preview_container'); // unchanged
        
        // إخفاء جميع عناصر المعاينة أولاً
        const allPreviews = mediaContainer.querySelectorAll('img, video, audio, #file_info');
        allPreviews.forEach(el => el.style.display = 'none');
        document.getElementById('no_media_msg').style.display = 'block';

        if (fileInput.files && fileInput.files[0]) {
            const file = fileInput.files[0];
            const fileType = file.type.split('/')[0];
            
            // إخفاء رسالة عدم وجود ملف
            document.getElementById('no_media_msg').style.display = 'none';

            // معاينة حسب نوع الملف
            const reader = new FileReader();
            reader.onload = function(e) {
                switch(fileType) {
                    case 'image':
                        const imgPreview = document.getElementById('image_preview'); // unchanged
                        imgPreview.src = e.target.result;
                        imgPreview.style.display = 'block';
                        break;
                        
                    case 'video':
                        const videoPreview = document.getElementById('video_preview'); // unchanged
                        videoPreview.src = e.target.result;
                        videoPreview.style.display = 'block';
                        videoPreview.autoplay = false;
                        videoPreview.loop = false;
                        break;
                        
                    case 'audio':
                        const audioPreview = document.getElementById('audio_preview'); // unchanged
                        audioPreview.src = e.target.result;
                        audioPreview.style.display = 'block';
                        break;
                        
                    default:
                        const fileInfo = document.getElementById('file_info');
                        document.getElementById('file_name').textContent = file.name;
                        document.getElementById('file_type').textContent = file.type;
                        fileInfo.style.display = 'block';
                }
            };
            
            reader.readAsDataURL(file);
        }

        // موقع البلاغ
        const locationTexts = {
            'classroom': 'قاعة دراسية',
            'computer_lab': 'معمل الحاسب الآلي',
            'library': 'المكتبة',
            'main_hall': 'القاعة الكبرى',
            'blue_hall': 'القاعة الزرقاء',
            'meeting_room': 'قاعة الاجتماعات',
            'agriculture_lab': 'معمل الزراعة',
            'administrative_office': 'مكتب إداري',
            'clinic': 'العيادة',
            'cafeteria': 'البوفيه',
            'male_restrooms': 'حمامات الطلاب',
            'female_restrooms': 'حمامات الطالبات',
            'girls_lounge': 'استراحة البنات',
            'girls_garden': 'حديقة البنات',
            'mosque': 'المسجد',
            'football_field': 'ملعب كرة القدم',
            'parking_lot': 'المواقف',
            'corridor': 'الممر',
            'staff_restrooms': 'حمامات الموظفين',
            'campus': 'الحرم الجامعي'
        };

        // تم تعديل id ليتطابق مع القالب (#selected_location_view)
        const locationValue = $('input[name="locationRadio"]:checked').val();
        $('#selected_location_view').text(locationTexts[locationValue] || "لم يتم تحديد الموقع");

        // تصنيف البلاغ
        const categoryTexts = {
            'cleanliness': 'نظافة',
            'harassment': 'تحرش',
            'theft': 'سرقة',
            'verbal_abuse': 'تلفظ',
            'blackmail': 'ابتزاز',
            'threat': 'تهديد',
            'kidnapping': 'خطف',
            'vandalism': 'تخريب',
            'incitement': 'تحريض',
            'assault': 'اعتداء',
            'accident': 'حادث',
            'disturbance': 'ازعاج',
            'terrorism': 'إرهاب',
            'fire': 'حريق',
            'fraud': 'احتيال',
            'bribery': 'رشوة',
            'bullying': 'تنمر'
        };

        // تم تعديل id ليتطابق مع القالب (#selected_category_view)
        const categoryValue = $('input[name="categoryRadio"]:checked').val();
        $('#selected_category_view').text(categoryTexts[categoryValue] || "لم يتم تحديد النوع");

        // وصف البلاغ
        const description = $('.description_input').val();
        $('#description_display').val(description);

        // بيانات المبلغ
        const reporter_name = $('.reporter_name_input').val();
        $('#reporter_name_display').val(reporter_name);

        const phone_number = $('.phone_number_input').val();
        $('#phone_number_display').val(phone_number);

        // لا يوجد حقل password في القالب لذلك تم حذف الكود المتعلق به
    },

    _onCloseModal: function() {
        const videoPreview = document.getElementById('video_preview');
        const audioPreview = document.getElementById('audio_preview');
        
        if (videoPreview) {
            videoPreview.pause();
            videoPreview.currentTime = 0;
        }
        
        if (audioPreview) {
            audioPreview.pause();
            audioPreview.currentTime = 0;
        }
    }
    
});
