import hashlib
import datetime

# Transaction class to represent a simple transfer of value
class Transaction:
    def __init__(self, sender, receiver, amount):
        # Initialize transaction with sender, receiver, and amount
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def __str__(self):
        # String representation for hashing purposes
        return f"{self.sender} -> {self.receiver}: {self.amount}"

# Block class to represent a block in the blockchain
class Block:
    def __init__(self, index, timestamp, transactions, previous_hash):
        # Initialize block attributes
        self.index = index                  # Position in the chain
        self.timestamp = timestamp          # Time of block creation
        self.transactions = transactions    # List of Transaction objects
        self.previous_hash = previous_hash  # Hash of the previous block
        self.nonce = 0                      # Nonce for proof-of-work
        self.hash = self.calculate_hash()   # Initial hash (updated during mining)

    def calculate_hash(self):
        # Calculate the SHA-256 hash of the block
        #The miner solves a puzzle with hashing 
        # Concatenate all block attributes as strings and hash them
        sha = hashlib.sha256()
        sha.update(str(self.index).encode('utf-8') +
                   str(self.timestamp).encode('utf-8') +
                   ''.join([str(tx) for tx in self.transactions]).encode('utf-8') +
                   str(self.previous_hash).encode('utf-8') +
                   str(self.nonce).encode('utf-8'))
        return sha.hexdigest()

    def mine_block(self, difficulty):
        # Perform proof-of-work to find a nonce that satisfies the difficulty
        # The hash must start with 'difficulty' number of zeros
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block {self.index} mined: {self.hash} (nonce: {self.nonce})")

# Blockchain class to manage the chain of blocks
class Blockchain:
    def __init__(self):
        # Initialize the blockchain with a fixed difficulty and genesis block
        self.difficulty = 4  # Number of leading zeros required in the hash
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        # Create and mine the genesis block (first block in the chain)
        genesis_block = Block(0, datetime.datetime(2009, 1, 1), [], "0")
        genesis_block.mine_block(self.difficulty)
        return genesis_block

    def get_last_block(self):
        # Return the most recent block in the chain
        return self.chain[-1]

    def add_block(self, transactions):
        # Add a new block to the chain with the given transactions
        previous_block = self.get_last_block()
        new_index = previous_block.index + 1
        new_timestamp = datetime.datetime.now()
        new_block = Block(new_index, new_timestamp, transactions, previous_block.hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)

    def is_chain_valid(self):
        # Verify the integrity and validity of the blockchain
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]
            # Check if the stored hash matches the recalculated hash
            if current_block.hash != current_block.calculate_hash():
                print(f"Invalid hash at block {i}")
                return False
            # Check if the previous_hash links to the previous block's hash
            if current_block.previous_hash != previous_block.hash:
                print(f"Invalid previous hash at block {i}")
                return False
            # Verify proof-of-work
            if current_block.hash[:self.difficulty] != '0' * self.difficulty:
                print(f"Proof-of-work invalid at block {i}")
                return False
        return True

# Example usage to demonstrate the blockchain
if __name__ == "__main__":
    # Create a new blockchain instance
    blockchain = Blockchain()

    # Create and add a block with some transactions
    tx1 = Transaction("Alice", "Bob", 10)
    tx2 = Transaction("Bob", "Charlie", 5)
    print("Mining block 1...")
    blockchain.add_block([tx1, tx2])

    # Add another block with a transaction
    tx3 = Transaction("Charlie", "David", 3)
    print("Mining block 2...")
    blockchain.add_block([tx3])

    # Display the blockchain
    print("\nBlockchain contents:")
    for block in blockchain.chain:
        tx_list = [str(tx) for tx in block.transactions]
        print(f"Block {block.index}:")
        print(f"  Hash: {block.hash}")
        print(f"  Nonce: {block.nonce}")
        print(f"  Previous Hash: {block.previous_hash}")
        print(f"  Transactions: {tx_list}")
        print(f"  Timestamp: {block.timestamp}")

    # Verify the chain
    print("\nVerifying blockchain integrity...")
    is_valid = blockchain.is_chain_valid()
    print(f"Blockchain valid: {is_valid}")
