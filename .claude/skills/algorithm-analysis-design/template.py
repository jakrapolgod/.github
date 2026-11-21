"""
ตัวอย่างเต็มตามโครงสร้างบังคับของวิชา Analysis and Design of Algorithms

โจทย์: Coin Change (จำนวนเหรียญน้อยที่สุด)
  มีเหรียญหลายชนิด (ใช้ชนิดละกี่เหรียญก็ได้) ต้องการทอนเงินจำนวน amount
  ให้ใช้เหรียญน้อยที่สุด ถ้าทอนไม่ได้ให้ตอบ -1

Input : coins (list[int], ทุกค่า >= 1, ไม่ซ้ำ), amount (int >= 0)
Output: จำนวนเหรียญน้อยที่สุด หรือ -1

ข้อจำกัด: 1 <= len(coins) <= 100, 0 <= amount <= 10^4
  → งบเวลา: len(coins) * amount = 10^6 ทำได้ใน Python ภายใน 1 วินาที
    ดังนั้น O(amount * len(coins)) ผ่าน

Edge cases: amount = 0 (ตอบ 0), ทอนไม่ได้ (coins=[2], amount=3 → -1),
  มีเหรียญชนิดเดียว, เหรียญใหญ่กว่า amount ทั้งหมด,
  ชุดเหรียญที่ greedy ใช้ไม่ได้ (coins=[1,3,4], amount=6 → 2 ไม่ใช่ 3)
"""

import random
import time


# ---------------------------------------------------------------------------
# code แบบที่ AI มักให้มา: ดูสมเหตุสมผล รันได้ แต่ "ผิด"
# ---------------------------------------------------------------------------
def greedy_wrong(coins: list[int], amount: int) -> int:
    """เลือกเหรียญใหญ่ที่สุดก่อนเสมอ — ถูกเฉพาะชุดเหรียญ canonical เช่น [1,2,5,10]"""
    count = 0
    for c in sorted(coins, reverse=True):
        count += amount // c
        amount %= c
    return count if amount == 0 else -1


# ---------------------------------------------------------------------------
# [2] Brute force อ้างอิง: ลองทุกทางตามนิยาม — ช้า (exponential) แต่ถูกแน่นอน
# ---------------------------------------------------------------------------
def brute_force(coins: list[int], amount: int) -> int:
    def best(rest: int) -> float:
        if rest == 0:
            return 0
        return min((1 + best(rest - c) for c in coins if c <= rest),
                   default=float("inf"))

    ans = best(amount)
    return -1 if ans == float("inf") else int(ans)


# ---------------------------------------------------------------------------
# [3][4][5] วิธีจริง
# ---------------------------------------------------------------------------
def solve(coins: list[int], amount: int) -> int:
    """
    เทคนิค: Dynamic Programming แบบ bottom-up

    ความถูกต้อง (recurrence):
      state      : dp[x] = จำนวนเหรียญน้อยที่สุดที่รวมได้ x พอดี (INF ถ้าทำไม่ได้)
      base case  : dp[0] = 0
      transition : dp[x] = min(dp[x - c] + 1) สำหรับทุก c ใน coins ที่ c <= x
      เหตุผล     : คำตอบที่ดีที่สุดของ x ต้องมีเหรียญ "ใบสุดท้าย" สักใบ c
                   ส่วนที่เหลือ x - c ต้องเป็นคำตอบที่ดีที่สุดของ x - c ด้วย
                   (optimal substructure — ถ้าไม่ใช่ จะแทนด้วยทางที่ดีกว่าได้ ขัดแย้ง)
      ลำดับ      : x จาก 1 ถึง amount เพราะ dp[x] ใช้เฉพาะ dp ที่ index น้อยกว่า
      loop invariant: ก่อนรอบ x ค่า dp[0..x-1] ถูกต้องทั้งหมด

    Time : O(amount * len(coins)) — loop นอก amount รอบ, loop ใน len(coins) รอบ
    Space: O(amount)              — ตาราง dp ขนาด amount + 1
    """
    INF = amount + 1  # ใช้เหรียญไม่เกิน amount ใบ (เหรียญเล็กสุด >= 1)
    dp = [0] + [INF] * amount
    for x in range(1, amount + 1):
        for c in coins:
            if c <= x and dp[x - c] + 1 < dp[x]:
                dp[x] = dp[x - c] + 1
    return dp[amount] if dp[amount] != INF else -1


# ---------------------------------------------------------------------------
# [6] ทดสอบ: ตัวอย่าง + edge case
# ---------------------------------------------------------------------------
def test_examples() -> None:
    cases = [
        (([1, 2, 5], 11), 3),     # 5 + 5 + 1
        (([2], 3), -1),           # ทอนไม่ได้
        (([1], 0), 0),            # amount = 0
        (([7], 14), 2),           # เหรียญชนิดเดียว
        (([5, 10], 3), -1),       # เหรียญใหญ่กว่า amount ทั้งหมด
        (([1, 3, 4], 6), 2),      # greedy ได้ 3 (4+1+1) แต่คำตอบคือ 3+3
    ]
    for (coins, amount), expected in cases:
        got = solve(coins, amount)
        assert got == expected, f"solve{coins, amount} = {got}, expected {expected}"
    print(f"[test_examples] ผ่าน {len(cases)} กรณี")


def stress_test(fn, trials: int = 3000, seed: int = 1) -> bool:
    """สุ่ม input เล็ก ๆ เทียบกับ brute_force แล้วรายงาน counterexample ตัวแรกที่เจอ"""
    rng = random.Random(seed)
    for _ in range(trials):
        coins = rng.sample(range(1, 11), rng.randint(1, 4))
        amount = rng.randint(0, 25)
        want, got = brute_force(coins, amount), fn(coins, amount)
        if want != got:
            print(f"[stress_test] {fn.__name__} ผิด: coins={coins}, amount={amount}"
                  f" → ได้ {got}, ที่ถูกคือ {want}")
            return False
    print(f"[stress_test] {fn.__name__} ผ่าน {trials} ชุดสุ่ม")
    return True


# ---------------------------------------------------------------------------
# [7] วัดประสิทธิภาพ: amount โตเป็นเท่าตัว → เวลาควรโต ~2 เท่า (เชิงเส้นใน amount)
# ---------------------------------------------------------------------------
def benchmark() -> None:
    coins = list(range(1, 101))  # len(coins) = 100 ซึ่งเป็นค่าสูงสุด
    prev = None
    for amount in (1250, 2500, 5000, 10000):
        t = time.perf_counter()
        solve(coins, amount)
        dt = time.perf_counter() - t
        ratio = f"  (x{dt / prev:.2f})" if prev else ""
        print(f"[benchmark] amount={amount:>6}: {dt:.3f}s{ratio}")
        prev = dt


if __name__ == "__main__":
    test_examples()
    stress_test(greedy_wrong)  # คาดว่าไม่ผ่าน — แสดงว่า code ที่ "ดูถูก" ผิดได้
    assert stress_test(solve)
    benchmark()
