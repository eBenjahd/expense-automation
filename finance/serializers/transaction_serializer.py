from rest_framework import serializers
from .account_serializer import AccountSerializer
from .category_serializer import CategorySerializer
from finance.models import Transaction, Category, Account


class TransactionSerializer(serializers.ModelSerializer):

    account = AccountSerializer(required=False, allow_null=True)
    category = CategorySerializer()

    class Meta:

        model = Transaction
        fields = [
            "id",
            "account",
            "category",
            "kind",
            "amount",
            "currency",
            "description",
            "raw_text",
            "source",
            "occurred_at",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "raw_text",
            "source",
            "created_at",
        ]

    def create(self, validated_data):

        account_data = validated_data.pop("account", None)
        category_data = validated_data.pop("category", None)
        user = validated_data.pop("user")

        if account_data:
            account_name = account_data["name"].strip().lower()

            account, _ = Account.objects.get_or_create(
                user=user,
                name=account_name
            )
        else:
            account, _ = Account.objects.get_or_create(
                user=user,
                name="Efectivo"
            )

        if category_data:

            category_name = category_data["name"].strip().lower()

            category, _ = Category.objects.get_or_create(
                user=user,
                name=category_name,
                kind=category_data["kind"]
            )
        else:
            category = None

        return Transaction.objects.create(
            user=user,
            account=account,
            category=category,
            **validated_data
        )
    
    def update(self, instance, validated_data):

        account_data = validated_data.pop("account", None)
        category_data = validated_data.pop("category", None)

        # KIND
        kind = validated_data.get("kind", instance.kind)

        # ACCOUNT
        if account_data:
            account_name = account_data["name"].strip().lower()

            account, _ = Account.objects.get_or_create(
                user=instance.user,
                name=account_name
            )

            instance.account = account

        # CATEGORY
        if category_data:
            category_name = category_data["name"].strip().lower()

            category, _ = Category.objects.get_or_create(
                user=instance.user,
                name=category_name,
                kind=kind
            )

            instance.category = category

        # RESTO DE CAMPOS
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance