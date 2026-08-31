def fifo(pages, frames):
    memory = []
    hits = 0
    misses = 0

    for page in pages:
        if page in memory:
            hits += 1
            print(page, "-> HIT", memory)
        else:
            misses += 1

            if len(memory) < frames:
                memory.append(page)
            else:
                memory.pop(0)
                memory.append(page)

            print(page, "-> MISS", memory)

    print("\nFIFO Hits:", hits)
    print("FIFO Misses:", misses)


def lru(pages, frames):
    memory = []
    hits = 0
    misses = 0

    for page in pages:
        if page in memory:
            hits += 1
            memory.remove(page)
            memory.append(page)
            print(page, "-> HIT", memory)
        else:
            misses += 1

            if len(memory) == frames:
                memory.pop(0)

            memory.append(page)
            print(page, "-> MISS", memory)

    print("\nLRU Hits:", hits)
    print("LRU Misses:", misses)


pages = list(map(int, input("Enter page reference string: ").split()))
frames = int(input("Enter number of frames: "))

print("\n--- FIFO Page Replacement ---")
fifo(pages, frames)

print("\n--- LRU Page Replacement ---")
lru(pages, frames)
