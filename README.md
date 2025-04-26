# 📦 Docker Backup Script
Скрипт для **резервного копирования Docker-проектов**, написанный на Python.  
 Позволяет:
- Останавливать контейнеры из выбранных `docker-compose.yml`
- Архивировать указанные каталоги
- Исключать каталоги из архивации
- Перезапускать контейнеры после завершения
- Работать через Anaconda-окружение для портативности
## 🛠 Установка
1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/22crystyle/docker-backup-script.git
   cd docker-backup-script
   ```
2. Установите зависимости через [Anaconda](https://www.anaconda.com/):
   ```bash
   conda env create -f environment.yml
   conda activate backup_env
   ```
## ⚙️ Конфигурация
Настройте файл `config.json`:
```json
{
  "backup_dir": "../backups",
  "directories": [
    "./path/to/your/project",
    "./another/path"
  ],
  "exclude_dirs": [
    "./path/to/your/project/excluded_folder"
  ],
  "compose_dir": "./compose_links",
  "stop_containers": true,
  "restart_containers": true
}
```
| Параметр           | Описание                                             |
|--------------------|------------------------------------------------------|
| `backup_dir`         | Папка, куда сохранять архивы                         |
| `directories`        | Каталоги для архивации                               |
| `exclude_dirs`       | Каталоги для исключения                              |
| `compose_dir`        | Путь к папке со **ссылками** на файлы `docker-compose.yml` |
| `stop_containers`    | Останавливать контейнеры перед бэкапом               |
| `restart_containers` | Перезапустить контейнеры после бэкапа                |

**Важно:** в папке `compose_dir` должны находиться **символические ссылки** на файлы `docker-compose.yml`.
## 🚀 Запуск
Активируйте окружение и запустите скрипт:
```bash
conda activate backup_env
sudo python backup.py
```
## 📝 Логи
- Все действия скрипта пишутся в файл `log.txt`.
- В логах отмечается:
  - Какие директории добавлены в архив
  - Какие директории пропущены
  - Ошибки (например, если путь не найден)
  - Состояние остановки/запуска контейнеров
  - Завершение скрипта
## ❓ FAQ:
**Q:** Нужно ли иметь права `sudo`?  
 **A:** Да, если требуется остановить/запустить Docker-контейнеры.
 
**Q:** Можно ли использовать без Anaconda?  
 **A:** Можно, установив `pyyaml` через pip:
 
```bash
pip install pyyaml
```
но Anaconda облегчает переносимость окружения.
## ©️ Лицензия
MIT License — свободное использование и модификация.
