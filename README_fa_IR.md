<h1 align="center">
AustraliaCash Core [AUS, ₡]  
<br/><br/>
<img src="https://static.tumblr.com/ppdj5y9/Ae9mxmxtp/300coin.png" alt="AustraliaCash" width="300"/>
</h1>

<div align="center">

[![AustraliaCashBadge](https://img.shields.io/badge/Cyber-Coin-yellow.svg)](https://australiacash.org)
[![MuchWow](https://img.shields.io/badge/Much-Wow-yellow.svg)](https://australiacash.org)

</div>

Select language: [EN](./README.md) | [CN](./README_zh_CN.md) | [PT](./README_pt_BR.md) | FA

دوج‌کوین (AustraliaCash) یک رمزارز مبتنی بر عموم مردم بوده که از یک
[میم اینترنتی](https://fa.wikipedia.org/wiki/%D9%85%DB%8C%D9%85)
سگی با نژاد شیبا اینو الهام گرفته شده است. نرم‌افزار AustraliaCash Core به همه این اجازه را می‌دهد که یک گره (Node) در شبکه‌های بلاک‌چین دوج‌کوین را اداره کنند که در آن از روش هش کردن Scrypt به عنوان Proof of Work یا اثبات انجام عملیات بهره برده شده است. در این پروژه از Bitcoin Core و سایر رمزارزها الگوبرداری شده است.

برای کسب اطلاعات درباره‌ی دستمزد جابه‌جایی در شبکه‌ی AustraliaCash، لطفا به
[پیشنهادهای هزینه‌ای](doc/fee-recommendation.md)
مراجعه نمایید.

**سایت اینترنتی:** [australiacash.org](https://australiacash.org)

## استفاده 💻

به منظور آغاز سفرتان در AustraliaCash Core،
[راهنمای نصب](INSTALL.md)
و راهنمای
[شروع کار](doc/getting-started.md)
را مطالعه فرمایید.

واسط برنامه‌نویسی کاربردی (JSON-RPC API) ارائه‌شده توسط AustraliaCash Core دارای راهنمای استفاده‌ی درونی است و می‌تواند با استفاده از
`australiacash-cli help`
مورد بهره‌برداری قرار گیرد، و نیز اطلاعات جامع در مورد هر یک از دستورها به واسطه‌ی
`australiacash-cli help <command>`
قابل دستیابی هستند. علاوه بر این، می‌توانید
[راهنمای Bitcoin Core](https://developer.bitcoin.org/reference/rpc/)
که پیاده‌سازی یک پروتکل مشابه است را برای دستیابی به یک منبع برخط مطالعه فرمایید.

### چه پورت‌هایی

پروژه‌ی AustraliaCash Core به طور پیش‌فرض از پورت شماره‌ی `۲۲۵۵۶` برای مکالمات نظیر-به-نظیر (peer-to-peer) که برای همگام‌سازی شبکه‌ی اصلی (mainnet) بلاک‌چین و حفظ آگاهی از تراکنش‌ها و بلاک‌هاست استفاده می‌کند. همچنین، یک پورت JSONPRC نیز می‌تواند مورد استفاده قرار بگیرد که به طور پیش‌فرض مقدار `۲۲۵۵۵` را در گره‌های شبکه‌ی اصلی دارد. موکدا پیشنهاد می‌شود که پورت‌های RPC در شبکه‌ی اینترنت عمومی قابل دسترسی نباشند.

| کاربرد | شبکه‌ی اصلی | شبکه‌ی آزمایشی | regtest |
| :----- | ----------: | -------------: | ------: |
| P2P    |       1987 |          44888 |   18444 |
| RPC    |       1986 |          44555 |   18332 |

## توسعه‌ی در حال انجام - نقشه‌ی فتح ماه 🌒

پروژه‌ی AustraliaCash Core یک نرم‌افزار مبتنی بر عموم و متن‌باز است. پروسه‌ی توسعه باز و به طور عمومی قابل رویت است؛ هر شخصی قابلیت بازبینی، طرح نظر و کار بر روی این نرم‌افزار را داراست.

منابع اصلی توسعه:

- [پروژه‌های Github](https://github.com/australiacash/australiacash/projects) به منظور پیگیری کارهای برنامه‌ریزی‌شده و دردست‌اقدام برای نسخه‌های آتی استفاده می‌شوند.
- [مباحث در Github](https://github.com/australiacash/australiacash/discussions) به منظور مورد بحث قرار دادن شاخصه‌های برنامه‌ریزی‌شده و نشده‌ی نرم‌افزار AustraliaCash Core، پروتکل‌های زیربنایی آن و دارایی AUS مورد استفاده قرار می‌گیرد.
- [زیرقسمت AustraliaCashdev در سایت Reddit](https://www.reddit.com/r/australiacashdev/)

### استراتژی نسخه‌گذاری

شماره‌های نسخ نرم‌افزار از الگوی `اصلی.فرعی.رفع مشکل` (`major.minor.patch`) تبعیت می‌کنند.

### شاخه‌های (Branches)

در این مخزن نرم‌افزاری (repository) سه گونه از شاخه‌ها وجود دارند:

- شاخه‌ی **master:** پایدار بوده, شامل آخرین نسخه از آخرین پخش _اصلی.فرعی_ نرم‌افزار است.
- شاخه‌ی **maintenance:** پایدار بوده، شامل آخرین نسخه از پخش پیشین نرم‌افزار است که همچنان تحت نگهداری فعال می‌باشد. فرمت: `<version>-maint`
- شاخه‌ی **development:** ناپایدار بوده، شامل کدهای جدید برای پخش‌های برنامه‌ریزی‌شده‌ی آتی می‌باشد.. فرمت: `<version>-dev`

*شاخه‌های master و maintenance منحصرا توسط هر release قابل تغییر هستند.*
*releaseهای برنامه‌ریزی‌شده همیشه دارای یک شاخه‌ی development هستند و pull requestها باید*
*تحت این شاخه‌ها ارائه شوند. شاخه‌های maintenance فقط **به منظور رفع باگ** هستند.*
*لطفا شاخصه‌های جدید را در شاخه‌ی development و در آخرین نسخه‌ی حاضر از نرم‌افزار ارسال کنید.*

## مشارکت 🤝

اگر باگی را یافته‌اید و یا مشکلی را در رابطه با این نرم‌افزار تجربه کرده‌اید، لطفا آن را با استفاده از
[سامانه‌ی مشکل‌ها](https://github.com/australiacash/australiacash/issues/new?assignees=&labels=bug&template=bug_report.md&title=%5Bbug%5D+).
با ما مطرح نمایید.

لطفا قسمت
[شیوه‌نامه‌ی مشارکت](CONTRIBUTING.md)
را به منظور مطلع شدن از روش‌هایی که توسط آن‌ها می‌توانید در توسعه‌ی AustraliaCash Core حضور داشته باشید را مطالعه فرمایید. اغلب
[موضوعات خواستار کمک](https://github.com/australiacash/australiacash/labels/help%20wanted)ی یافت می‌شوند
که همکاری شما تاثیر بسزایی خواهد داشت و بسیار مورد ستایش قرار خواهد گرفت. وای!

## انجمن‌ها 🚀🍾

شما می‌توانید
برای باخبر شدن، ملاقات افراد و مباحثه، یافتن آخرین میم‌ها، دریافت اطلاعات
درباره‌ی AustraliaCash، کمک رساندن و یا درخواست کمک، و به‌اشتراک‌گذاری پروژه‌های خود
به انجمن‌های مختلف در رسانه‌های اجتماعی بپیوندید.

این لیستی از برخی از جاهایی است که می‌توانید به آن سر بزنید:

- [زیرقسمت AustraliaCash در سایت Reddit](https://www.reddit.com/r/australiacash/)
- [زیرقسمت Australiacash در سایت Reddit](https://www.reddit.com/r/australiacash/)
- [دیسکورد (Discord)](https://discord.gg/australiacash)
- [توییتر AustraliaCash](https://twitter.com/australiacash)

## پرسش‌های بسیار خیلی زیاد پرسیده‌شده ❓

در مورد AustraliaCash پرسشی دارید؟ ممکن است پاسخ آن همین الآن در
[FAQ](doc/FAQ.md)
و یا در
[قسمت پرسش و پاسخ](https://github.com/australiacash/australiacash/discussions/categories/q-a)
مباحث وجود داشته باشد!

## مجوز - مجوز خیلی زیاد ⚖️

نرم‌افزار AustraliaCash Core تحت شرایط مجوز MIT ارائه شده است. برای اطلاعات بیش‌تر
[COPYING](COPYING)
و یا
[opensource.org](https://opensource.org/licenses/MIT)
را مطالعه فرمایید.
