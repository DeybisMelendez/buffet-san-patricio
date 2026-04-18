from django import forms

from .models import ProductIngredient, Table


class ProductIngredientForm(forms.ModelForm):
    """Formulario para editar ingredientes de una receta."""

    class Meta:
        model = ProductIngredient
        fields = ["ingredient", "quantity"]
        widgets = {
            "ingredient": forms.Select(attrs={"class": "form__control"}),
            "quantity": forms.NumberInput(
                attrs={"class": "form__control", "step": "0.01", "min": "0"}
            ),
        }

    def __init__(self, *args, **kwargs):
        self.product = kwargs.pop("product", None)
        super().__init__(*args, **kwargs)
        # Ordenar ingredientes alfabéticamente y mostrar nombre con unidad
        self.fields["ingredient"].queryset = self.fields[
            "ingredient"
        ].queryset.order_by("name")
        self.fields["ingredient"].label_from_instance = lambda obj: obj.name_with_unit()

    def clean(self):
        cleaned_data = super().clean()
        ingredient = cleaned_data.get("ingredient")

        # Si tenemos producto (nueva instancia) validar duplicados
        if self.product and ingredient:
            # Verificar si ya existe una receta con este producto e ingrediente
            # excluyendo la instancia actual (si la hay)
            existing = ProductIngredient.objects.filter(
                product=self.product,
                ingredient=ingredient,
            )
            if self.instance.pk:
                existing = existing.exclude(pk=self.instance.pk)

            if existing.exists():
                raise forms.ValidationError(
                    f"El ingrediente '{ingredient.name}' ya está en la receta de este producto."
                )

        return cleaned_data


class TableForm(forms.ModelForm):
    """Formulario para crear y editar mesas."""

    class Meta:
        model = Table
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form__control", "placeholder": "Nombre de la mesa"}
            ),
        }

    def clean_name(self):
        name = self.cleaned_data.get("name")
        if not name:
            raise forms.ValidationError("El nombre de la mesa es obligatorio.")
        existing = Table.objects.filter(name=name)
        if self.instance.pk:
            existing = existing.exclude(pk=self.instance.pk)
        if existing.exists():
            raise forms.ValidationError("Ya existe una mesa con este nombre.")
        return name.upper()
