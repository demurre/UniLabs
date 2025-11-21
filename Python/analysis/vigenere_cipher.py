class VigenereCipher:
    """
    Vigenere cipher - polyalphabetic substitution cipher.
    """

    def __init__(self, key: str):
        """Initializes the cipher with a key."""
        if not key:
            raise ValueError("Key cannot be empty")
        self.key = key.upper()

    @staticmethod
    def _char_to_num(char: str) -> int:
        """Converts a character to a number (0-25)."""
        return ord(char.upper()) - ord("A")

    @staticmethod
    def _num_to_char(num: int) -> str:
        """Converts a number (0-25) to a character."""
        return chr((num % 26) + ord("A"))

    def _get_key_char(self, position: int) -> str:
        """Gets the key character at the given position."""
        return self.key[position % len(self.key)]

    def encrypt(self, plaintext: str) -> str:
        """
        Encrypts text using the Vigenere cipher.
        Only encrypts letters, special characters remain unchanged.
        """
        ciphertext = []
        key_position = 0

        for char in plaintext:
            if char.isalpha():
                char_num = self._char_to_num(char)
                key_num = self._char_to_num(self._get_key_char(key_position))
                encrypted_num = (char_num + key_num) % 26
                encrypted_char = self._num_to_char(encrypted_num)
                if char.islower():
                    encrypted_char = encrypted_char.lower()
                ciphertext.append(encrypted_char)
                key_position += 1
            else:
                ciphertext.append(char)

        return "".join(ciphertext)

    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypts text using the Vigenere cipher.
        """
        plaintext = []
        key_position = 0

        for char in ciphertext:
            if char.isalpha():
                char_num = self._char_to_num(char)
                key_num = self._char_to_num(self._get_key_char(key_position))
                decrypted_num = (char_num - key_num) % 26
                decrypted_char = self._num_to_char(decrypted_num)
                if char.islower():
                    decrypted_char = decrypted_char.lower()
                plaintext.append(decrypted_char)
                key_position += 1
            else:
                plaintext.append(char)

        return "".join(plaintext)

    @staticmethod
    def generate_key_from_password(password: str, length: int = 10) -> str:
        """
        Generates a Vigenere key from a password.
        """
        if not password:
            raise ValueError("Password cannot be empty")

        letters = "".join(c for c in password if c.isalpha()).upper()

        if not letters:
            raise ValueError("Password must contain at least one letter")

        key = (letters * ((length // len(letters)) + 1))[:length]
        return key
