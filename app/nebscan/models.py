from django.db import models, IntegrityError
from django.db.models.signals import pre_save


class NebBlock(models.Model):
    GENESIS_HASH = (
        '0000000000000000000000000000000000000000000000000000000000000000')

    hash = models.CharField(max_length=64, primary_key=True)
    parent = models.OneToOneField('self', on_delete=models.PROTECT)
    height = models.PositiveIntegerField(unique=True)
    nonce = models.PositiveIntegerField()
    timestamp = models.IntegerField()
    miner = models.CharField(max_length=64, db_index=True)
    coinbase = models.CharField(max_length=48, db_index=True)
    is_finality = models.BooleanField(default=False)

    @property
    def parent_hash(self):
        return self.parent.hash if self.parent_id else self.GENESIS_HASH

    @property
    def is_genesis(self):
        return self.hash == self.GENESIS_HASH

    @classmethod
    def pre_save(cls, sender, instance, **kwargs):
        try:
            instance.parent
        except cls.DoesNotExist:
            raise IntegrityError(
                f'Parent block {instance.parent_id} does not exist')


pre_save.connect(NebBlock.pre_save, sender=NebBlock, weak=False)


class NebAddress(models.Model):
    address = models.CharField(max_length=64, primary_key=True)
    balance = models.DecimalField(max_digits=50, decimal_places=0)
    nonce = models.PositiveIntegerField()
    address_type = models.SmallIntegerField()


class NebTransaction(models.Model):
    hash = models.CharField(max_length=64, primary_key=True)
    block_hash = models.ForeignKey('NebBlock', on_delete=models.PROTECT)
    from_address = models.ForeignKey(
        'NebAddress', on_delete=models.PROTECT,
        related_name='out_transaction_set')
    to_address = models.ForeignKey(
        'NebAddress', on_delete=models.PROTECT,
        related_name='in_transaction_set')
    value = models.DecimalField(max_digits=50, decimal_places=0)
    nonce = models.PositiveIntegerField()
    timestamp = models.IntegerField()
    transaction_type = models.CharField(max_length=64, db_index=True)
    data = models.TextField(null=True)
    gas_price = models.PositiveIntegerField()
    gas_limit = models.PositiveIntegerField()
    gas_used = models.PositiveIntegerField()
    contract_address = models.ForeignKey(
        'NebAddress', on_delete=models.PROTECT, null=True,
        related_name='contract_address_set')
    status = models.SmallIntegerField()
    execute_error = models.TextField(default='')
    execute_result = models.TextField(default='')
