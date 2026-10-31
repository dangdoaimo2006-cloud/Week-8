# Phan tich yeu cau

## Bai toan
He thong theo doi remote may chieu, remote dieu hoa va micro khong day. Thiet bi tu phat su kien; cac dich vu nhan su kien se duoc bo sung o cac giai doan sau.

## Publisher va subscriber
- Publisher: `TeachingDevice` va cac lop ke thua.
- Subscriber: dich vu thong bao, bao tri, ghi nhat ky va bo loc canh bao (chua cai dat o giai doan 2).
- Publisher khong phu thuoc truc tiep vao subscriber.

## Event data
`StatusChanged`: `DeviceId`, `OldStatus`, `NewStatus`, `ChangedAt`.

`AlertRaised`: `DeviceId`, `Message`, `Severity`, `OccurredAt`.

## Quy tac nghiep vu
- Trang thai: `Available`, `Borrowed`, `UnderMaintenance`.
- Muc do: `Information`, `Warning`, `Critical`.
- Remote may chieu: pin duoi 20% la Warning; pin bang 0 la Critical.
- Remote dieu hoa: chuyen tu co phan hoi sang mat phan hoi la Critical.
- Micro: pin duoi 30% hoac tin hieu duoi 40% la Warning; pin bang 0 hoac tin hieu bang 0 la Critical.
- Khong phat lap lai neu chi so van nam trong cung vung canh bao.
- Khong phat `StatusChanged` neu trang thai moi trung trang thai hien tai.

## Pham vi giai doan 2
Hien thuc hoa enum, event args, lop publisher co so va ba lop thiet bi. Subscriber, delegate loc canh bao, coordinator va exception rieng nam trong cac giai doan sau.
