from collections import OrderedDict
from django import forms
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Submit
from .models import CourseSides, MainCourse, Patient, Sides, Purchase, PurchaseDetail, Supplier, RfidCard, MealOrderTimeSlot
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User,Group
from django import forms

# class NewMedicineForm(forms.ModelForm):
#     class Meta:
#         model = Medicine
#         fields = ['medicine_name', 'efficacy', 'side_effects', 'min_stock_level']
#         labels = {
#             'medicine_name': '藥品名稱',
#             'efficacy': '功效',
#             'side_effects': '副作用',
#             'min_stock_level': '最低庫存量',
#         }
#         error_messages = {
#             'medicine_name': {'required': '藥品名稱不可為空'},
#             'efficacy': {'required': '功效不可為空'},
#             'side_effects': {'required': '副作用不可為空'},
#             'min_stock_level': {'required': '最低庫存量不可為空'},
#         }

#     def clean_min_stock_level(self):
#         min_stock_level = self.cleaned_data.get('min_stock_level')
#         if min_stock_level is not None and min_stock_level <= 0:
#             raise ValidationError('最低庫存量不可為0')
#         return min_stock_level



# class NewPurchase(forms.ModelForm):
#     class Meta:
#         model = Purchase
#         fields = ['medicine', 'purchase_date', 'purchase_q', 'purchase_unit_price']
#         labels = {
#             'medicine': '藥品名稱',
#             'purchase_date': '進貨日期',
#             'purchase_q': '進貨數量',
#             'purchase_unit_price': '進貨單價',
#         }
#         error_messages = {
#             'medicine': {'required': '藥品名稱不可為空'},
#             'purchase_date': {'required': '進貨日期不可為空'},
#             'purchase_q': {'required': '進貨數量不可為空'},
#             'purchase_unit_price': {'required': '進貨單價不可為空'},
#         }

#     def clean_purchase_q(self):
#         purchase_q = self.cleaned_data.get('purchase_q')
#         if purchase_q is not None and purchase_q <= 0:
#             raise ValidationError('最低進貨數量不可為0')
#         return purchase_q
      
#     def clean_purchase_unit_price(self):
#         purchase_unit_price = self.cleaned_data.get('purchase_unit_price')
#         if purchase_unit_price is not None and purchase_unit_price <= 0:
#             raise ValidationError('最低進貨單價不可為0')
#         return purchase_unit_price


# class WarehouseCreationForm(forms.ModelForm):
#     class Meta:
#         model = Warehouse
#         fields = ['medicine', 'creation_date', 'is_active']
#         labels = {
#             'medicine': '藥品名稱',
#             'creation_date': '創建日期',
#             'is_active': '是否啟用',
#            }
#         widgets = {
#             'creation_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
#             'medicine': forms.Select(attrs={'class': 'form-control'}),
#             'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'})
#         }

# class WarehouseFilterForm(forms.Form):
#     medicine_name = forms.ModelChoiceField(
#         queryset=Medicine.objects.all(),
#         label='藥品名稱',
#         required=False,
#         empty_label='--- 不篩選 ---'  
#     )
#     is_active = forms.BooleanField(label='是否啟用', required=False)


class SelectorForm(forms.ModelForm):
    patients = forms.ModelMultipleChoiceField(
        queryset=Patient.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control choices'}),
        required=True,
        label="選擇發送對象"
    )
    
    notify_message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        label="通知訊息"
    )

    class Meta:
        model = Notify
        fields = ['notify_message', 'patients']

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='必填，請輸入有效的郵件地址。')
    first_name = forms.CharField(max_length=30, required=True, help_text='必填')
    last_name = forms.CharField(max_length=30, required=True, help_text='必填')
    groups = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=True,
        help_text='選擇用戶所屬的群組'
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'groups')

    def clean_groups(self):
        groups = self.cleaned_data.get('groups')
        if not groups:
            raise forms.ValidationError("必須選擇一個群組。")
        return groups

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_active = 1
        user.is_superuser = 0
        user.is_staff = 0
        if commit:
            user.save()
            user.groups.set([self.cleaned_data['groups']])
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "姓氏"
        self.fields['last_name'].label = "名字"

class UserEditForm(forms.ModelForm):
    groups = forms.ModelChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="請選擇該用戶的群組。",
        empty_label="無群組"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'groups']

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['groups'].label_from_instance = self.label_from_instance
        if self.instance and self.instance.pk and self.instance.groups.exists():
            self.fields['groups'].initial = self.instance.groups.first()

        self.fields['first_name'].label = "姓氏"
        self.fields['last_name'].label = "名字"
        self.fields['groups'].label = "權限"

    def label_from_instance(self, obj):
        return obj.display
    
class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['patient_name', 'patient_birth', 'patient_number','patient_idcard']
        widgets = {
            'patient_birth': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(PatientForm, self).__init__(*args, **kwargs)
        self.fields['patient_name'].label = "被照護者姓名"
        self.fields['patient_birth'].label = "出生年月日"
        self.fields['patient_number'].label = "電話號碼"
        self.fields['patient_idcard'].label = "身分證字號"
        
class PatientFormEdit(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['patient_name', 'patient_birth', 'patient_number','patient_idcard','line_id']
        widgets = {
            'patient_birth': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(PatientFormEdit, self).__init__(*args, **kwargs)
        self.fields['patient_name'].label = "被照護者姓名"
        self.fields['patient_birth'].label = "出生年月日"
        self.fields['patient_number'].label = "電話號碼"
        self.fields['patient_idcard'].label = "身分證字號"
        self.fields['line_id'].label = "LineUID"

class RfidCardForm(forms.ModelForm):
    class Meta:
        model = RfidCard
        fields = ['rfidCard_code', 'patient']
        
    def __init__(self, *args, **kwargs):
        super(RfidCardForm, self).__init__(*args, **kwargs)
    
        self.fields['rfidCard_code'].label = "卡片內碼"
        self.fields['patient'].label = "被照護者"

        self.fields['rfidCard_code'].disabled = True

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['supplier_name', 'supplier_number']

    def __init__(self, *args, **kwargs):
        super(SupplierForm, self).__init__(*args, **kwargs)

        self.fields['supplier_name'].label = "供應商名稱"
        self.fields['supplier_number'].label = "供應商電話"

class MainCourseForm(forms.ModelForm):
    timeSlot = forms.ModelChoiceField(queryset=MealOrderTimeSlot.objects.all(), empty_label=None)
    class Meta:
        model = MainCourse
        fields = ['course_name', 'course_price', 'course_image', 'timeSlot']

    def __init__(self, *args, **kwargs):
        super(MainCourseForm, self).__init__(*args, **kwargs)

        self.fields['course_name'].label = "主餐名稱"
        self.fields['course_price'].label = "價格"
        self.fields['course_image'].label = "圖片"
        self.fields['timeSlot'].label = "開放時段"

class CourseSidesForm(forms.ModelForm):
    class Meta:
        model = CourseSides
        fields = ['course', 'sides', 'quantity']
        
    def __init__(self, *args, **kwargs):
        super(CourseSidesForm, self).__init__(*args, **kwargs)
        
        self.fields['course'].label = "主菜名稱"
        self.fields['sides'].label = "食材"
        self.fields['quantity'].label = "數量"

        # 調整字段的widget
        self.fields['course'].widget.attrs.update({
                    'class': 'form-select',
                    'placeholder': '選擇主菜'
        })
        self.fields['sides'].widget.attrs.update({
            'class': 'form-select',
            'placeholder': '選擇食材'
        })
        self.fields['quantity'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': '輸入數量'
        })

                # self.helper = FormHelper()
        # self.helper.layout = Layout(
        #     Row(
        #         Column('course', css_class='form-group col-md-6 mb-0'),
        #         css_class='row'
        #     ),
        #     Row(
        #         Column('sides', css_class='form-group col-md-6 mb-0'),
        #         css_class='row'
        #     ),
        #     Row(
        #         Column('quantity', css_class='form-group col-md-6 mb-0'),
        #         css_class='row'
        #     ),
        #     Submit('submit', '保存', css_class='btn btn-primary')

class MealOrderTimeSlotForm(forms.ModelForm):
    class Meta:
        model = MealOrderTimeSlot
        fields = ['timeSlot_name', 'startTime', 'deadlineTime', 'endTimes']
        widgets = {
            'timeSlot_name': forms.TextInput(attrs={'class': 'form-control'}),
            'startTime': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'deadlineTime': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'endTimes': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        }
        labels = {
            'timeSlot_name': '時段名稱',
            'startTime': '開始時間',
            'deadlineTime': '點餐截止時間',
            'endTimes': '結束時間',
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('startTime')
        deadline_time = cleaned_data.get('deadlineTime')
        end_time = cleaned_data.get('endTimes')
        
        errors = []

        if start_time and deadline_time and end_time:
            if not (start_time < deadline_time < end_time):
                errors.append(ValidationError('時間順序不正確: 結束時間必須大於點餐截止時間，且點餐截止時間必須大於開始時間'))
            
            formatted_time_1 = start_time.strftime("%H:%M")
            formatted_time_2 = deadline_time.strftime("%H:%M")
            formatted_time_3 = end_time.strftime("%H:%M")
            
            overlapping_slot_check1 = MealOrderTimeSlot.objects.filter(startTime__lte=start_time, endTimes__gte=start_time).exclude(pk=self.instance.pk).exists()
            overlapping_slot_check2 = MealOrderTimeSlot.objects.filter(startTime__lte=deadline_time, endTimes__gte=deadline_time).exclude(pk=self.instance.pk).exists()
            overlapping_slot_check3 = MealOrderTimeSlot.objects.filter(startTime__lte=end_time, endTimes__gte=end_time).exclude(pk=self.instance.pk).exists()
            
            if overlapping_slot_check1:
                errors.append(ValidationError(f'開始時段 {formatted_time_1} 與其他時段重疊，請選擇其他時間範圍'))
            if overlapping_slot_check2:
                errors.append(ValidationError(f'點餐結束時段 {formatted_time_2} 與其他時段重疊，請選擇其他時間範圍'))
            if overlapping_slot_check3:
                errors.append(ValidationError(f'結束時段 {formatted_time_3} 與其他時段重疊，請選擇其他時間範圍'))

        if errors:
            raise ValidationError(errors)

        return cleaned_data

class PurchaseDetailForm(forms.ModelForm):
    sides_id = forms.ModelChoiceField(
        queryset=Sides.objects.all(),
        required=False,
        label='食材選擇',
        help_text='選擇新的食材'
    )
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.all(),
        required=True,
        label='供應商選擇',
        help_text='選擇供應商'
    )
    purchase_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='進貨日期',
        help_text='選擇進貨日期'
    )
    # sides_unit = forms.CharField(
    #     max_length=45, 
    #     required=False, 
    #     label='單位', 
    #     disabled=True  # 這個字段僅用於顯示，不用於提交
    # )

    class Meta:
        model = PurchaseDetail
        fields = ['purchase_quantity', 'purchase_date']

    def __init__(self, *args, **kwargs):
        super(PurchaseDetailForm, self).__init__(*args, **kwargs)
        
        self.fields['purchase_quantity'].label = "進貨數量"

        # 定義欄位順序
        new_order = OrderedDict()
        new_order['sides_id'] = self.fields['sides_id']
        new_order['supplier'] = self.fields['supplier']
        new_order['purchase_date'] = self.fields['purchase_date']
        new_order['purchase_quantity'] = self.fields['purchase_quantity']
        # new_order['sides_unit'] = self.fields['sides_unit']
        self.fields = new_order

    def save(self, commit=True):
        sides_id = self.cleaned_data.get('sides_id')
        if sides_id:
            self.instance.sides = sides_id
        
        supplier = self.cleaned_data.get('supplier')
        purchase, created = Purchase.objects.get_or_create(supplier=supplier)
        self.instance.purchase = purchase
        
        return super().save(commit=commit)

class AddSides(forms.ModelForm):
    class Meta:
        model = Sides
        fields = ['sides_name', 'sides_unit']

    def __init__(self, *args, **kwargs):
        super(AddSides, self).__init__(*args, **kwargs)

        self.fields['sides_name'].label = "食材名稱"
        self.fields['sides_unit'].label = "單位"