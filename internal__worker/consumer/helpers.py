import hashlib
import time


class PoW:
    """Алгоритм майнинга Proof of Work"""

    MAX_NONCE = 2**32  # 4 billion

    def __init__(self, message: str) -> None:
        self.message = message

    async def proof_of_work(
        self,
        header: str,
        difficulty_bits: int,
    ) -> str | tuple:
        """Доказательство работы

        Args:
            header (str): заголовок для шифрования
            difficulty_bits (int): биты сложности
        """
        # calculate the difficulty target
        target = 2 ** (256 - difficulty_bits)

        for nonce in range(self.MAX_NONCE):
            encode_to_bytes = (str(header) + str(nonce)).encode()
            hash_result = hashlib.sha256(encode_to_bytes).hexdigest()

            # check if this is a valid result, below the target
            if int(hash_result, 16) < target:
                print((f"Success with nonce {nonce}"))
                print((f"Hash is {hash_result}"))
                return hash_result, nonce

        print((f"Failed after {nonce} (max_nonce) tries"))
        return nonce

    async def calculate(self):
        """Основной расчет алгоритма"""
        nonce = 0
        hash_result = ""

        # difficulty from 0 to 31 bits
        test_range = 22
        calculate_start_time = time.time()
        for difficulty_bits in range(test_range):
            difficulty = 2**difficulty_bits
            print((f"Difficulty: {difficulty} ({difficulty_bits} bits)"))

            print("Starting search...")

            # checkpoint the current time
            start_time = time.time()

            # make a new block which includes the hash from the previous block
            # we fake a block of transactions - just a string
            new_block = self.message + hash_result

            # find a valid nonce for the new block
            hash_result, nonce = await self.proof_of_work(
                new_block,
                difficulty_bits,
            )

            # checkpoint how long it took to find a result
            end_time = time.time()

            elapsed_time = end_time - start_time
            print((f"Elapsed Time: {elapsed_time:.4f} seconds"))

            if elapsed_time > 0:
                # estimate the hashes per second
                hash_power = float(int(nonce) / elapsed_time)
                print((f"Hashing Power: {hash_power} hashes per second"))

        calculate_elapsed_time = time.time() - calculate_start_time
        return hash_result, calculate_elapsed_time
