from rest_framework import serializers


class ContentTypeRestrictedValidator(object):
    def __call__(self, file):
        try:
            content_type = file.content_type
            if content_type in self.serializer_field.content_types:
                if file.size > self.serializer_field.max_upload_size:
                    raise serializers.ValidationError(
                        f"O tamanho máximo permitido é {filesizeformat(self.serializer_field.max_upload_size)}. Tamanho atual: {filesizeformat(file.size)}"
                    )
            else:
                raise serializers.ValidationError("Arquivo deve ser um PDF.")
        except AttributeError:
            pass
        return file

    def set_context(self, serializer_field):
        self.serializer_field = serializer_field


class ContentTypeRestrictedFileField(serializers.FileField):
    default_validators = [ContentTypeRestrictedValidator()]

    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types")
        self.max_upload_size = kwargs.pop("max_upload_size")

        super().__init__(*args, **kwargs)
