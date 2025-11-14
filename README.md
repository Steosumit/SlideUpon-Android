# SlideUpon - Android Productivity App
A application that forms the extension of the [Screetime app](https://sites.google.com/view/screetime), built as a hobby project to reduce eye strain issues: Computer Vision Syndrome 
> Initially proprietary; happly made open sourced!
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![Kivy](https://img.shields.io/badge/Framework-Kivy-brightgreen.svg)](https://kivy.org/)

**SlideUpon** is an Android-based productivity application designed to help users complete tasks efficiently with calculated work-break schedules. The app combines research-based time management techniques with personalized health monitoring to optimize your workflow.

🌐 **Website**: [https://sites.google.com/view/screetime/slideupon](https://sites.google.com/view/screetime/slideupon?authuser=0)

---

## 📋 Table of Contents

- [Features](#-features)
- [Time Management Techniques](#-time-management-techniques)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Configuration](#-configuration)
- [Dependencies](#-dependencies)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## ✨ Features

### Core Functionality
- **Multiple Time Management Algorithms**
  - AppName Algorithm (Recommended) - Custom algorithm with task categorization
  - Pomodoro Technique - Classic 25-minute intervals
  - 60/10 Method - 60 minutes of work followed by 10 minutes of mind wandering

- **Smart Break Calculation**
  - Automatic break duration calculation based on interval length
  - Eye strain prevention using the 20-20-20 rule
  - Blink rate monitoring and adjustment
  - Movement reminders to prevent sedentary behavior

- **Task Categories**
  - PC or Mobile Related Tasks
  - Study Sessions
  - Limited Time Tasks
  - Mind Wandering Sessions

### Health & Wellness Features
- **Blink Test**: Measures your eye blink rate to calculate optimal screen break times
- **Flow State Detection**: Tests and tracks your maximum focused work duration
- **Exhaustion Limit Tracking**: Monitors daily usage with three levels (Mild, Moderate, Extreme)
- **Habit Maker Reminders**: 
  - Posture correction alerts
  - Water drinking reminders
  - Walking/movement suggestions

### Progress Tracking
- **Real-time Progress Monitoring**: Track time spent on different task categories
- **Daily Usage Statistics**: Monitor today's work duration
- **Weekly/Monthly/Fortnightly Reports**: Customizable progress tracking periods
- **Performance Score**: Tracks improvement over time

### Customization
- **Theme Picker**: Choose from multiple color palettes and themes (Light/Dark)
- **Custom Intervals**: Set your own work and break durations
- **Auto Timer**: Automatically manages multiple intervals with calculated breaks
- **Audio Notifications**: Custom sound alerts for breaks and interval completion

---

## 🎯 Time Management Techniques

### 1. AppName Algorithm (RECOMMENDED)
A proprietary algorithm that adapts to your work type and health metrics:

**PC or Mobile Related Tasks**:
- Considers screen exposure time
- Factors in blink rate for eye health
- Applies 20-20-20 rule (every 20 minutes, look at something 20 feet away for 20 seconds)
- Includes movement breaks

**Study Tasks**:
- Optimized for learning and retention
- Includes quick revision prompts (at 80% of interval time)
- Balances focused study with necessary breaks

**Limited Time Tasks**:
- High-intensity work sessions
- Flexible break scheduling for tight deadlines

### 2. Pomodoro Technique
- Traditional 25-minute work intervals
- Breaks scale with interval duration
- Every 4th break is extended

### 3. 60/10 Method
- 60 minutes of focused work
- 10 minutes of mind wandering/creative thinking
- Fixed interval structure

---

## 🚀 Installation

### Prerequisites
- Python 3.9 or higher
- Android device (for mobile deployment) or PC for testing

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/Steosumit/SlideUpon-Android.git
   cd SlideUpon-Android
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python NewApp.py
   ```

### Building for Android

For Android deployment, use Buildozer:

```bash
buildozer android debug
buildozer android deploy run
```

---

## 📱 Usage

### Getting Started

1. **Initial Setup**
   - Launch the app
   - Take the Blink Test to calibrate eye health monitoring
   - (Optional) Take the Flow Limit Test to find your optimal focus duration

2. **Starting a Work Session**
   - Navigate to the Main tab
   - Select a time management technique from the dropdown
   - Choose a task category (if using AppName Algorithm)
   - Enter interval duration (in minutes)
   - For auto mode: Enable the auto timer switch and enter total duration
   - Click START

3. **During Work Intervals**
   - Progress bar shows current interval status
   - Timer displays elapsed time (Hours : Minutes : Seconds)
   - Today's Use shows cumulative work time

4. **Break Management**
   - Audio notification signals break start
   - Dialog shows recommended break duration
   - Audio notification signals break end
   - Acknowledge dialog to stop reminder beeps

### Options Tab Features

- **Flow Limit Test**: Determine your maximum sustained focus time
- **Theme Picker**: Customize app appearance
- **Blink Rate**: View and update your average blink count
- **Audio Settings**: Select custom break notification sounds (MP3/WAV)

### Records Tab Features

- View progress by task category
- Track against weekly/monthly/fortnightly goals
- Monitor exhaustion limits
- Adjust progress measurement periods

---

## 📂 Project Structure

```
SlideUpon-Android/
├── NewApp.py              # Main application file with UI classes
├── app_manager.py         # Backend logic for breaks, settings, records
├── New.kv                 # Kivy UI definition file
├── Kivy.py               # Kivy configuration
├── records.dat           # User progress data (auto-generated)
├── settings.dat          # User preferences (auto-generated)
├── Fonts/                # Custom font files
│   ├── normal_font.otf
│   └── digital_font.ttf
├── Music/                # Audio notification files
│   ├── break_time.mp3
│   ├── break_over.mp3
│   ├── study_revise_*.mp3
│   └── beep_on.wav
└── Extra_Files/          # UI assets (GIFs, images)
    ├── posture.gif
    ├── drinkwater.gif
    └── walk.gif
```

---

## ⚙️ Configuration

### Data Files

**records.dat** - Stores user progress data:
- Total work hours
- Today's usage
- Task category breakdown
- Date tracking for daily resets

**settings.dat** - Stores user preferences:
- Theme settings (primary, accent, style)
- Audio file path
- Flow limit value
- Blink rate data
- Progress tracking configuration
- Exhaustion limit thresholds

### Customizable Parameters

You can modify these in the Options tab:
- Flow time usage (enable/disable)
- Exhaustion limit monitoring (enable/disable)
- Progress measurement period (Weekly/Monthly/Fortnightly/Custom)
- Progress limit (hours per period)

---

## 📦 Dependencies

```
kivy>=2.1.0
kivymd>=1.0.0
pygame>=2.1.0
playsound>=1.3.0
beepy>=1.0.7
plyer>=2.0.0
kivy-garden>=0.1.4
```

Install all dependencies with:
```bash
pip install kivy kivymd pygame playsound beepy plyer kivy-garden
```

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Areas for Contribution
- Bug fixes and improvements
- UI/UX enhancements
- Additional time management techniques
- Localization/translations
- Documentation improvements
- Testing on various Android devices

---

## 📄 License

This project is currently unlicensed. Please contact the author for usage permissions.

---

## 📧 Contact

**Developer**: Sumit Gupta

**Email**: sgsonu132@gmail.com

**Project Link**: [https://github.com/Steosumit/SlideUpon-Android](https://github.com/Steosumit/SlideUpon-Android)

**Website**: [https://sites.google.com/view/screetime/slideupon](https://sites.google.com/view/screetime/slideupon?authuser=0)

---

## 🙏 Acknowledgments

- Research-based on Flow State psychology
- Eye health guidelines from the 20-20-20 rule
- Pomodoro Technique principles
- Kivy and KivyMD framework communities

---

## ⚠️ Known Issues

- MCI initialization error with some audio files (use MP3 or WAV format)
- File chooser is optimized for PC; mobile version uses different file picker
- Some features marked for next version (e.g., extended Pomodoro break selection)

---

## 🔮 Future Enhancements

- Cloud sync for progress data
- Statistics visualization with charts
- Social features for accountability
- Integration with calendar apps
- Customizable habit maker reminders
- Export progress reports

---

**Made with ❤️ in India**
