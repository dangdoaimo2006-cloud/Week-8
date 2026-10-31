# Week 8 - Delegate & Event (Python)

Tien do: Giai doan 2/5.

Da cai dat enum, event args, `TeachingDevice` va ba lop thiet bi. Cac phuong thuc dang ky/huy dang ky callback da co; publisher khong giu tham chieu toi cac dich vu subscriber.

Chua cai dat subscriber services, `FilteredAlertSubscriber`, `DeviceMonitoringCoordinator`, exception rieng, `main.py` va bo test tong the. Cac phan nay se duoc lam o giai doan tiep theo.

## Chay thu
Tu thu muc du an:

```bash
python -c "import sys; sys.path.insert(0, 'src'); from teaching_devices import ProjectorRemote; d=ProjectorRemote('P01','Remote may chieu'); d.add_alert_raised_handler(lambda s,e: print(e.message)); d.update_battery_level(15)"
```

Handler nhan hai tham so: doi tuong phat event va event args. Python khong co cu phap `event` nhu C#, nen danh sach callback duoc quan ly ben trong `TeachingDevice`.
