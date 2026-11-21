# กติกาการเขียน code ใน repo นี้

ทุก code ที่เป็นอัลกอริทึม (โจทย์แข่งขัน, การบ้าน, การตรวจ code ที่ AI สร้าง)
ต้องทำตาม skill `algorithm-analysis-design`
(`.claude/skills/algorithm-analysis-design/SKILL.md`) ทุกครั้ง โดยย่อคือ:

1. สเปกโจทย์ + ข้อจำกัด + งบเวลา + edge case
2. brute force อ้างอิง
3. วิธีที่มีประสิทธิภาพ พร้อมบอกเทคนิค
4. เหตุผลความถูกต้อง (invariant / recurrence / exchange argument)
5. Time และ Space แบบ Big-O พร้อมที่มา
6. test ตัวอย่าง + stress test เทียบ brute force
7. benchmark ที่ขนาด input โตเป็นเท่าตัว

ต้องรัน test และ benchmark จริงแล้วรายงานผลก่อนบอกว่าเสร็จ
ตัวอย่างโครงสร้างเต็ม: `.claude/skills/algorithm-analysis-design/template.py`
