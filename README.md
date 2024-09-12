# Family-expenses-organizer-Application
UPDATE: CURRENT DESCRIPTION

Family-expenses-organizer-Application  is an application that helps to follow your expenses and spare your money.
It offers user possibilities as follows:
1) To registrate data about expenses (date, sum spended, category of expense). Current expenses, past expenses and future expenses can be registrated.
2) To set limits (spare goals). You can set a limit sum for yourself as a spare goal. You can add several limits. The dates of your limits can be in the current time, in the past time and also in the future. Only one spare goal (limit) will be be an ACTIVE LIMIT.. Active spare goal is always in the current time or in the future time. If the limit is active it means that:

1) you will see warnings calculated on the basis of your active limit and your expenses.
2) you will see “sum you can freely spend” calculated on the basis of your active limit and your expenses made during this active limit is enabled.
3) you will be able to registrate extra data about expenses (subjective estimation)
Active limit has history=0 value in column history in limits table.

Your non-active limits (can be of 2 kinds:
1) Limits that initially were added as active but before the end date of the limit was reached were cancelled (replaced by a new active limit). These limits will not be considered in any way for analysis. They don`t affect Balance. They won`t produce warnings anymore.  The “sum you can freely spend” will not consider such limit anymore. Input of extra data about expenses (subjective estimation) will not be possible for such non-active limits.

2) Limits that are not active anymore because the end date of the limit is less than today date. These limits are considered for analysis: they affect Balance,  the chart can be made to visualize this limit data, extra data about expenses can be registrated. Warnings will not be made as the purpose of warnings is taking your current and future expenses under control.

3) Limits that were initially added as “history” limits. Their dates were initially in the past time. These limits are considered for analysis: they affect Balance,  the chart can be made to visualize this limit data, extra data about expenses can be registrated. Warnings will not be made as the purpose of warnings is taking your current and future expenses under control.

Non-active limits have history=1 value in column history in limits table.

3) To set warning sum on the basis of your ACTIVE limit. When this sum is reached you start to see warnings. If you set no warning sum, warning sum equal or greater than your limit than you start to get warnings immediately.
After reaching warning sum (or immediately in the situations with no warning sum, warning sum equal or greater warning sum) you will get warnings every time you make an expense. These warning will provide you with information about the sum up to the limit or if the limit is exceeded -  about the sum beyond the limit.

All warnings you see are considering only your ACTIVE limit. If you have no active limit you will not see any warnings.

4) to follow spare balance. Spare balance unites spare logica and motivation beyond that of just the limits itself. Spare balance is recalculated when the limit becomes “historical”, in other words, when the period of limit ends or if the limit is initially created in the past time. Spare balance is not recalculated during expenses made outside spare goals periods or during ACTIVE limit. The sense of following spare balance is that it helps you to be consecutive in sparing money and follow some general sparing idea. If your spare goal was unsuccessful this time, have a look at your spare balance, maybe it shows that it`s not all that bad according to general spare results.

5) to set application individually for yourself. You can select between LIGHT and DARK mode, you can select between 3 variants of currency. Specifying currency will be applied to output, it will not recalculate expenses and all spare results and statistics.

6) and, of course, to save all your input data if you are a signed up user and sign in for the current session.

7) to get insights about expenses per category in the specified period of time (pie-chart).
   
8) to make input of your data in a comfortable way. For example, you can select date of expense in several ways.



Further course of development of this application:
to add possibility to get insights about subjective estimation of spending money according to your spare goal that now can be added after registrating an expense having been made in the ACTIVE or NON-ACTIVE BUT STATISTICALLY ELIGIBLE LIMITS(not replaced before the date of the limit expires). An app now calculates and saves statistical data (for example, AVERAGE of such subjective estimations. It also calculates “real success rate” on the basis of fulfilling spare goal when limit period expires. The comparison will be put out as a chart.


END UPDATE

![flet_WkpJCnaCXB](https://github.com/user-attachments/assets/beb07957-e489-4911-8b10-6d39e808c7b5)

![flet_Zbtteku4mG](https://github.com/user-attachments/assets/2c142c21-25d7-49ee-b715-6a201065187e)

![flet_kk02JfBpPW](https://github.com/user-attachments/assets/649e3c61-724a-4f12-8013-77888c91d5b1)


![flet_QR7FHyswck](https://github.com/user-attachments/assets/2d69408c-46c5-4ca1-93ea-975ed81ba66b)


Application that has following functionality:
1) Selecting the category of expenses
2) Input of the sum of money spent. Input the date of the expenses.
3) Specifying your goals for a selected period of time regarding sapring money
4) Selecting the subjective level of your certainty of having your expenses in accordance with your spare goals specified before
5) Creating charts for getting insights of the relationship between real expenses, the financial goals and the subjective feeling of going along with the spare goals during period of time selected for the goals.
6) Creating charts for getting more insights in spending money for different purposes during selected period of time.
7) Saving all the data typed in (dates, expenses, spare goals)
8) Some encouraging an cheer-up messages during using the application to make it more interactive and pleasant to use.
9) User-friendly design, especially for general functionalities - making selecting date posiible in several ways, making selecting categories of expenses and data input simple and quick to find and to fulfill.
10) Possibility to make input for future planned expenses, previous expenses
