
# Hashly 🔒

**Hashly** is a lookup tool designed to quickly determine if a given hash has been precomputed—**it does not crack hashes in real time**.  
[Check it out](https://hashly.duckdns.org/)

---

### How Hashly Works

1. **Database Generation:**  
   Instead of gathering hashes from public internet sources, Hashly currently builds its database using the [rockyou.txt](https://wiki.skullsecurity.org/index.php?title=Passwords) wordlist. For each password in this list, Hashly generates hashes using several algorithms:  
   - **SHA-1**  
   - **SHA-256**  
   - **SHA-512**  
   - **NTLM**  
   - **bcrypt**  
   - **scrypt**  
   - **PBKDF2**  
   - **MD5**

2. **Indexing with Typesense:**  
   The generated hashes—along with their corresponding plaintext passwords and hash format—are saved in a text file. Hashly then uses [Typesense](https://typesense.org) to index this data, enabling fast and efficient searches.

3. **Lookup Functionality:**  
   When you paste a hash into Hashly:
   - **If the hash exists in the index:**  
     Hashly returns the plaintext password and shows the hash format.
   - **If the hash is not found:**  
     Hashly provides guidance on possible methods to crack it and additional information about the hash type.

---

## Features

- Search hashes via CLI or web interface  
- Secured with HTTPS (DuckDNS + Let’s Encrypt)  
- Dockerized deployment

---

## Quick Start

- [Read Part 1: Guide.md](https://github.com/doany1/Hashly-/blob/c6c2df18d3c2336408990d02d7a55f5b408a4ddd/Part1/Guide.md)
- [Read Part 2: Guide.md](https://github.com/doany1/Hashly-/blob/c6c2df18d3c2336408990d02d7a55f5b408a4ddd/Part2/Guide.md)

---

## Disclaimer

Hashly is provided for educational and research purposes only. It is not a tool for unauthorized access or malicious activities. The tool does not perform live hash cracking; it only looks up precomputed hashes based on the rockyou.txt wordlist. Use it responsibly.

---

## Contributing

Contributions are welcome! If you have ideas, improvements, or bug fixes, please open an issue or submit a pull request.

---

## License

[MIT License](LICENSE)

---
