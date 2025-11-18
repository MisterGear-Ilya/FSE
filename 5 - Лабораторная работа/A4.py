def load_sequences(filename):
    """Считываем sequences.txt в словарь: {protein_name: (organism, sequence)}"""
    sequences = {}
    with open(filename, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            # Бывают лишние табы — ограничим разбиение до 3 полей
            parts = line.split("\t", maxsplit=2)
            if len(parts) != 3:
                parts = [p for p in line.split("\t") if p != ""]
                if len(parts) != 3:
                    continue
            protein, organism, seq = (parts[0].strip(), parts[1].strip(), parts[2].strip())
            sequences[protein] = (organism, seq)
    return sequences


def rle_decode(s: str) -> str:
    result = []
    i = 0
    n = len(s)
    while i < n:
        ch = s[i]
        if ch.isdigit():
            count = int(ch)
            # повторяем следующую букву count раз (если она есть)
            if i + 1 < n and s[i + 1].isalpha():
                result.append(s[i + 1] * count)
                i += 2
            else:
                # нет следующей буквы — игнорируем цифру
                i += 1
        else:
            # одиночная буква (или серия длины 1–2 без цифры)
            result.append(ch)
            i += 1
    return "".join(result)


def search(sequence, subseq):
    """Поиск subseq в последовательности"""
    return subseq in sequence


def diff(seq1, seq2):
    """Считаем различия между двумя последовательностями"""
    n = min(len(seq1), len(seq2))
    differences = sum(1 for i in range(n) if seq1[i] != seq2[i])
    differences += abs(len(seq1) - len(seq2))
    return differences


def mode_amino(seq):
    """Находим наиболее часто встречающуюся аминокислоту"""
    from collections import Counter
    counter = Counter(seq)
    max_count = max(counter.values())
    candidates = [aa for aa, cnt in counter.items() if cnt == max_count]
    return min(candidates), max_count


def solve():
    sequences = load_sequences("sequences.1.txt")

    with open("commands.1.txt", encoding="utf-8") as f:
        commands = [line.strip().split("\t") for line in f if line.strip()]

    with open("genedata1.txt", "w", encoding="utf-8") as out:
        out.write("Илья\n")
        out.write("Генетический поиск\n")

        for idx, cmd in enumerate(commands, start=1):
            op = cmd[0]
            out.write("-" * 74 + "\n")

            # Печатаем заголовок команды корректно:
            if op == "search":
                subseq = rle_decode(cmd[1])
                out.write(f"{idx:03d}   {op}   {subseq}\n")
            elif op == "diff":
                p1, p2 = cmd[1], cmd[2]
                out.write(f"{idx:03d}   {op}   {p1}   {p2}\n")
            elif op == "mode":
                protein = cmd[1]
                out.write(f"{idx:03d}   {op}   {protein}\n")
            else:
                # неизвестная команда — можно пропустить или вывести как есть
                out.write(f"{idx:03d}   {op}   " + "   ".join(cmd[1:]) + "\n")

            if op == "search":
                found = False
                out.write("organism\t\t\t\tprotein \n")
                for protein, (organism, seq) in sequences.items():
                    if search(seq, subseq):
                        out.write(f"{organism}\t\t{protein}\n")
                        found = True
                if not found:
                    out.write("NOT FOUND\n")

            elif op == "diff":
                p1, p2 = cmd[1], cmd[2]
                out.write("amino-acids difference:\n")
                missing = []
                if p1 not in sequences:
                    missing.append(p1)
                if p2 not in sequences:
                    missing.append(p2)
                if missing:
                    out.write("MISSING: " + ", ".join(missing) + "\n")
                else:
                    seq1 = sequences[p1][1]
                    seq2 = sequences[p2][1]
                    out.write(str(diff(seq1, seq2)) + "\n")

            elif op == "mode":
                protein = cmd[1]
                out.write("amino-acid occurs:\n")
                if protein not in sequences:
                    out.write("MISSING: " + protein + "\n")
                else:
                    seq = sequences[protein][1]
                    aa, cnt = mode_amino(seq)
                    out.write(f"{aa}\t\t  {cnt}\n")

        out.write("-" * 74 + "\n")


if __name__ == "__main__":
    solve()
