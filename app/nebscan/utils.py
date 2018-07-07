import json
from django.db import transaction

from nebpysdk.src.client.Neb import Neb

from nebscan.models import NebBlock


class Synchronizer:
    def __init__(self, provider='http://localhost:8685', api_version='v1'):
        self.neb = Neb(provider, api_version)

    def run(self) -> None:
        #FIXME
        for i in range(300000, 400000):
            print(i)
            self.sync_block(i)

    @staticmethod
    def parse_json(data: str) -> dict:
        return json.loads(data)['result']

    @staticmethod
    def create_neb_block(block: dict) -> NebBlock:
        neb_block = NebBlock(
            hash=block['hash'],
            parent_id=(block['parent_hash']
                       if block['hash'] != NebBlock.GENESIS_HASH else None),
            height=int(block['height']),
            nonce=int(block['nonce']),
            timestamp=int(block['timestamp']),
            miner=block['miner'],
            coinbase=block['coinbase'],
            is_finality=block['is_finality'])
        neb_block.save()

        return neb_block

    @transaction.atomic
    def sync_block(self, height: int) -> None:
        block_dct = self.get_block_by_height(height)
        neb_block = self.create_neb_block(block_dct)
        #FIXME
        for tx in block_dct['transactions']:
            import ipdb; ipdb.set_trace()  # TODO: FIX ME!
            pass

    def get_neb_state(self) -> dict:
        json_data = self.neb.api.getNebState().text
        neb_state = self.parse_json(json_data)

        return neb_state

    def get_neb_height(self) -> int:
        neb_state = self.get_neb_state()
        height = int(neb_state['height'])

        return height

    def get_block_by_height(self, height: int) -> dict:
        json_data = self.neb.api.getBlockByHeight(height).text
        block = self.parse_json(json_data)

        return block
