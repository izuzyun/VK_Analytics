#VK Analytics
«VK Analytics» — проект с открытым исходным кодом, позволяющий анализировать страницу сообщества в социальной сети «ВКонтакте». 
Данные получаются с помощью API ВКонтакте, а анализируются статистическим методом «двойное экспоненциальное сглаживание», которое позволяет выявить тренд, а также учитывать большую актуальность последних полученных данных, чем ранних. В данном случае такой анализ довольно точный, так как в подобных проектах хватает линейных методов. Если использовать модели машинного обучения, то они, вероятно, будут переобучены, а, следовательно, неточны.
Визуализация осуществляется с помощью библиотеки PyQtGraph, которая встраивается в интерфейс библиотеки PyQt.
Все используемые библиотеки проекта: bisect, time, sys, vk, PyQt5, NumPy, datetime.
