SELECT
    `都道府県`,
    COUNT(*) AS `件数`,
    SUM(`数量`) AS `数量合計`,
    SUM(`売上金額`) AS `売上合計`,
    AVG(`売上金額`) AS `平均売上`
FROM sales
GROUP BY `都道府県`
ORDER BY `売上合計` DESC;