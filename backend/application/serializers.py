from copy import deepcopy
from os import listdir, getcwd
from os.path import isfile, join
from rest_framework import serializers
from settings.models import Settings
from project.mixins import PrefetchMixin
from .fields import ContentTypeRestrictedFileField
from .boto_helper import upload
from .models import Application
import re


def get_form_option_choices():
    path = join(getcwd(), "application/choices/")
    choices = [f for f in listdir(path) if isfile(join(path, f)) and "__" not in f]
    return list(map(lambda x: x.split(".csv")[0], choices))


class ApplicationRetrieveSerializer(PrefetchMixin, serializers.ModelSerializer):
    unique_id = serializers.CharField(source="hacker.profile.unique_id")
    full_name = serializers.CharField(source="hacker.profile.shortcuts.full_name")
    email = serializers.CharField(source="hacker.profile.user.email")

    class Meta:
        model = Application
        exclude = ["hacker"]
        extra_fields = ["unique_id", "full_name", "email"]
        select_related_fields = ["hacker__profile__shortcuts", "hacker__profile__user"]

    def get_field_names(self, declared_fields, info):
        expanded_fields = super().get_field_names(declared_fields, info)

        if getattr(self.Meta, "extra_fields", None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields


class FormOptionChoicesSerializer(serializers.Serializer):
    option = serializers.ChoiceField(choices=get_form_option_choices())


class FormOptionSerializer(serializers.Serializer):
    text = serializers.CharField()
    value = serializers.CharField()


class FormOptionsSerializer(serializers.Serializer):
    success = serializers.BooleanField(default=True, required=False)
    results = FormOptionSerializer(many=True)


def format_phone(phone):
    phone = str(phone).strip()
    numbers = re.sub("[^0-9]", "", phone)
    pattern = re.compile(r"^\(?0?\d{2}\)?\s{0,}?\d{4,5}-?\d{4}$")
    if pattern.match(phone) is None:
        return None
    # (011)98888-8888 | (011)8888-8888
    if re.match(r"^0\d{2}\d{4,5}\d{4}$", numbers):
        if len(numbers) == 11:
            # (011)8888-8888
            numbers = f"({numbers[1:3]}){numbers[3:7]}-{numbers[7:11]}"
        else:
            # (011)98888-8888
            numbers = f"({numbers[1:3]}){numbers[3:8]}-{numbers[8:12]}"
    # (11)98888-8888 | (11)8888-8888
    else:
        if len(numbers) == 10:
            # (11)8888-8888
            numbers = f"({numbers[0:2]}){numbers[2:6]}-{numbers[6:10]}"
        else:
            # (11)98888-8888
            numbers = f"({numbers[0:2]}){numbers[2:7]}-{numbers[7:11]}"
    return numbers


class ApplicationSerializer(serializers.ModelSerializer):
    """Serialize and validate a hackers application"""

    first_name = serializers.CharField(
        max_length=50, label="Primeiro nome*", source="hacker.profile.user.first_name"
    )
    last_name = serializers.CharField(
        max_length=50,
        required=True,
        label="Sobrenome*",
        source="hacker.profile.user.last_name",
    )
    email = serializers.EmailField(
        required=True, label="Email*", source="hacker.profile.user.email"
    )
    file_cv = ContentTypeRestrictedFileField(
        allow_empty_file=False,
        content_types=["application/pdf"],
        max_upload_size=10485760,
        label="Arquivo com CV",
        required=False,
    )

    class Meta:
        model = Application
        exclude = ["hacker"]

    def validate_cv(self, data):
        cv = data
        if cv == "" or cv is None:
            return ""
        cv_type = self.initial_data.get("cv_type")
        if cv_type == "LI" and cv.find("linkedin.com/in/") < 0:
            cv = "https://linkedin.com/in/{}".format(cv)
        if cv_type == "GH" and cv.find("github.com/") < 0:
            cv = "https://github.com/{}".format(cv)
        if cv.find("://") < 0:
            cv = "https://{}".format(cv)
        return cv

    def validate_cv2(self, data):
        cv = data
        if cv == "" or cv is None:
            return ""
        cv_type = self.initial_data.get("cv2_type")
        if cv_type == "LI" and cv.find("linkedin.com/in/") < 0:
            cv = "https://linkedin.com/in/{}".format(cv)
        if cv_type == "GH" and cv.find("github.com/") < 0:
            cv = "https://github.com/{}".format(cv)
        if cv.find("://") < 0:
            cv = "https://{}".format(cv)
        return cv

    def validate_email(self, data):
        email = data
        pattern = re.compile("^temp_[0-9]+@email.com$")
        if pattern.match(email):
            raise serializers.ValidationError("Você precisa fornecer um email válido!")
        return email

    def validate_phone(self, data):
        phone = str(data).strip()
        numbers = re.sub("[^0-9]", "", phone)
        pattern = re.compile(r"^\(?0?\d{2}\)?\s{0,}?\d{4,5}-?\d{4}$")
        if pattern.match(phone) is None:
            message = "Celular inválido!"
            if len(numbers) < 10:
                message = "Será que falta o DDD?"
            raise serializers.ValidationError(message)
        numbers = format_phone(phone)
        return numbers

    def validate_school(self, data):
        school = data
        education = self.initial_data.get("education", "")
        if education not in ["Ensino Fundamental", "Ensino Médio"] and not school:
            raise serializers.ValidationError("Faculdade necessária")
        return school

    def validate_course(self, data):
        course = data
        education = self.initial_data.get("education", "")
        if education not in ["Ensino Fundamental", "Ensino Médio"] and not course:
            raise serializers.ValidationError("Curso necessário")
        return course

    def upload(self, data=None):
        file = data
        if not file:
            return
        try:
            url = upload(file.temporary_file_path())
        except Exception:
            raise serializers.ValidationError(
                {"file_cv": "Erro fazendo upload do arquivo"}
            )
        return url

    def validate(self, data):
        if data.get("cv_type") == "UP":
            file = data.get("file_cv", None)
            url = self.upload(file)
            if not url:
                raise serializers.ValidationError(
                    {"file_cv": ["Nenhum arquivo encontrado"]}
                )
            data["cv"] = url
        elif data.get("cv_type", False) and not data.get("cv", False):
            raise serializers.ValidationError({"cv": ["Nos fale seu currículo"]})

        if data.get("cv_type2", False) and not data.get("cv2", False):
            raise serializers.ValidationError({"cv2": ["Nos fale seu currículo"]})
        return data

    def save(self):
        data = deepcopy(self.validated_data)
        hacker_data = data.pop("hacker")
        profile_data = hacker_data["profile"]
        user_data = profile_data["user"]
        first_name = user_data["first_name"]
        last_name = user_data["last_name"]
        email = user_data["email"]
        data.pop("file_cv", None)

        hacker = self.context["hacker"]
        user = hacker.profile.user

        user.first_name = first_name
        user.last_name = last_name
        user.save()
        if email != user.email:
            user.profile.change_email(email)

        instance, _ = Application.objects.update_or_create(hacker=hacker, defaults=data)
        if Settings.get().auto_admit_hackers():
            hacker.admit(False)
        return instance
