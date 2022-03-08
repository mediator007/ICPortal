
############################# Add value to form #####################################
#Нашел решение. Реализовал контроллер-функцию вместо класса. А именно, вместо класса

class CommentForm(ModelForm):
    class Meta:
        model = models.Comment
        fields = ('author', 'content', 'bb')
        widgets = {'bb': forms.HiddenInput()}

    def __init__(self, bboard_id):
        super(CommentForm, self).__init__(self, bboard_id)
        self.fields['bb'] = models.Bb.objects.get(pk=bboard_id)


# Функция:
def new_comment(request, bboard_id):
    if request.method == 'POST':
        form = forms.CommentForm(request.POST, initial={'bb': Bb.objects.get(pk=bboard_id)})
        if form.is_valid():
            form.save(commit=False)
            form.bb = bboard_id
            form.save()
            return HttpResponseRedirect('http://localhost:8000/bboard/')
        else:
            context = {'form': form}
            return render(request, 'bboard/add_com.html', context)
    else:
        form = forms.CommentForm(initial={'bb': Bb.objects.get(pk=bboard_id)})
        context = {'form': form}
        return render(request, 'bboard/add_com.html', context)


# Договорные испытания. 2 Foreign Key. Проверку реализовать через функцию с декоратором 
#         @receiver(pre_save, sender=EquipmentWork) срабатывает перед сохранением и проверяет наличие
#         только одного ключа line_id или line_contract

from django.db.models.signals import pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=EquipmentWork)
def check_line(sender, instance, *args, **kwargs):
    # check that only one field True (line_id or line_contract)
    # т.е. что это именно создание, а не модификация
    if not instance.pk:             
       card = Card.objects.create(
            number = ...,           # тут должны быть значения полей
            pin_code = ...)
       instance.card = card