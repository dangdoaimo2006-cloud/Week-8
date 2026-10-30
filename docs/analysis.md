# Giai doan 1 - Phan tich nghiep vu va thiet ke

## 1. Bai toan nghiep vu
Truong dai hoc quan ly ba loai thiet bi trong phong day:
- Dieu khien may chieu.
- Dieu khien dieu hoa.
- Micro khong day.

Thiet bi co the thay doi trang thai, muc pin hoac chat luong tin hieu. Nhung thay doi nay can duoc thong bao den cac thanh phan khac nhau.

Cac thanh phan nhan thong tin:
- `ConsoleNotificationService`: hien thi canh bao.
- `MaintenanceService`: tao yeu cau bao tri khi co canh bao Critical.
- `DeviceAuditLogger`: ghi lich su thay doi trang thai.

Thiet bi chi phat hien va cong bo dieu da xay ra, khong goi truc tiep cac dich vu tren.

## 2. Publisher va subscriber
**Publisher:** `TeachingDevice` va ba lop dan xuat `ProjectorRemote`, `AirConditionerRemote`, `WirelessMicrophone`.

**Subscriber:** `ConsoleNotificationService`, `MaintenanceService`, `DeviceAuditLogger` va `FilteredAlertSubscriber`.

Mot event co the co nhieu subscriber; moi subscriber chi xu ly phan du lieu no quan tam.

## 3. Cac event

### `StatusChanged`
- `device_id`: ma thiet bi.
- `old_status`: trang thai cu.
- `new_status`: trang thai moi.
- `changed_at`: thoi diem thay doi.

Chi phat event neu trang thai moi khac trang thai hien tai. Cap nhat trang thai truoc, sau do moi thong bao.

### `AlertRaised`
- `device_id`: ma thiet bi.
- `message`: noi dung canh bao.
- `severity`: muc do canh bao.
- `occurred_at`: thoi diem phat sinh.

Muc do gom `Information`, `Warning`, `Critical`.

## 4. Quy tac cua tung thiet bi

### ProjectorRemote
- Pin tu 0 den 100.
- Pin duoi 20%: Warning.
- Pin bang 0%: Critical.
- Khong phat canh bao lap lai neu van o cung mot vung canh bao.

### AirConditionerRemote
- Co `assigned_room` va `is_responsive`.
- Chuyen tu dang phan hoi sang khong phan hoi: Critical.
- Khong lap lai canh bao neu trang thai van la khong phan hoi.

### WirelessMicrophone
- Pin va tin hieu tu 0 den 100.
- Pin duoi 30%: Warning.
- Tin hieu duoi 40%: Warning.
- Pin bang 0 hoac tin hieu bang 0: Critical.

## 5. Delegate va callback trong Python
Python khong co tu khoa `delegate` nhu C#. Trong project nay:
- `AlertFilter` duoc bieu dien bang callable nhan event args va tra ve `bool`.
- `action` la callable nhan event args va thuc hien mot hanh dong.
- `FilteredAlertSubscriber` goi filter; neu ket qua la True thi goi action.

## 6. Danh sach lop du kien

| Lop / kieu | Trach nhiem |
|---|---|
| `DeviceStatus` | Available, Borrowed, UnderMaintenance |
| `AlertSeverity` | Information, Warning, Critical |
| `DeviceStatusChangedEventArgs` | Du lieu event thay doi trang thai |
| `DeviceAlertEventArgs` | Du lieu event canh bao |
| `TeachingDevice` | Lop co so, quan ly trang thai va phat event |
| `ProjectorRemote` | Theo doi pin dieu khien may chieu |
| `AirConditionerRemote` | Theo doi kha nang phan hoi cua dieu khien dieu hoa |
| `WirelessMicrophone` | Theo doi pin va chat luong tin hieu |
| `ConsoleNotificationService` | Hien thi canh bao |
| `DeviceAuditLogger` | Ghi lich su thay doi trang thai |
| `MaintenanceService` | Tao yeu cau bao tri voi canh bao Critical |
| `FilteredAlertSubscriber` | Loc canh bao bang callable va goi action |
| `DeviceMonitoringCoordinator` | Quan ly dang ky va huy dang ky handler |
| `InvalidDeviceReadingException` | Loi khi pin/tin hieu ngoai [0, 100] |

## 7. Cac cau hoi thiet ke

### Vi sao thiet bi khong goi truc tiep MaintenanceService?
Lam nhu vay se tao phu thuoc truc tiep giua lop thiet bi va dich vu bao tri. Khi them logger, email hoac dashboard, lop thiet bi phai thay doi. Event giup publisher chi cong bo su kien, subscriber tu quyet dinh cach xu ly.

### Khi nao dung event rieng, khi nao dung chung?
`StatusChanged` va `AlertRaised` nen la hai event rieng vi y nghia va du lieu khac nhau. Canh bao pin thap va tin hieu yeu co the dung chung `AlertRaised`, vi cung co cau truc va muc dich thong bao; noi dung va severity phan biet tung truong hop.

### Ai co quyen phat sinh event?
Theo de bai, chi `TeachingDevice` va cac lop dan xuat duoc phat sinh event. Ben ngoai chi dang ky/huy dang ky handler. Trong Python, danh sach handler se duoc dong goi trong publisher, khong de ben ngoai thao tac truc tiep.

## 8. Cac diem can quy dinh khi cai dat
- Dung `Enum` cho trang thai va muc do canh bao.
- Dung lop rieng de chua du lieu event.
- Publisher quan ly danh sach callback cho tung event.
- Tranh dang ky trung handler va huy dung handler da dang ky.
- `DeviceMonitoringCoordinator` quan ly dang ky tap trung va co `dispose()`.
- Gia tri pin/tin hieu ngoai [0, 100] phat sinh `InvalidDeviceReadingException`.
- De bai chua quy dinh ro cach xu ly khi subscriber nem exception; se chot chinh sach o giai doan cai dat.
- De bai cho phep khong lap lai canh bao khi gia tri van o cung vung. Khi cai dat se theo doi viec chuyen vung canh bao de tranh lap.

## 9. Ke hoach 5 giai doan
1. Phan tich nghiep vu, publisher/subscriber, event, du lieu va UML.
2. Cai dat enum, event args, `TeachingDevice` va ba lop thiet bi.
3. Cai dat subscriber va `FilteredAlertSubscriber`.
4. Cai dat coordinator, subscribe/unsubscribe, dispose va ngoai le.
5. Cai dat `main.py`, kiem thu va hoan thien du an.
