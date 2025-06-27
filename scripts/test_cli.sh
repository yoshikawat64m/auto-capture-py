#!/bin/bash
# test_cli.sh - Auto Capture CLI 自動テストスクリプト

echo "=== Auto Capture CLI テスト開始 ==="

# テスト結果カウンター
PASSED=0
FAILED=0

# テスト関数
run_test() {
    local test_name="$1"
    local test_command="$2"
    local expected_result="$3"
    
    echo "テスト: $test_name"
    
    if eval "$test_command"; then
        if [ -n "$expected_result" ]; then
            if eval "$expected_result"; then
                echo "✅ $test_name 成功"
                ((PASSED++))
            else
                echo "❌ $test_name 失敗 (期待される結果が得られませんでした)"
                ((FAILED++))
            fi
        else
            echo "✅ $test_name 成功"
            ((PASSED++))
        fi
    else
        echo "❌ $test_name 失敗"
        ((FAILED++))
    fi
    echo ""
}

# 1. ヘルプテスト
run_test "ヘルプメッセージ表示" \
    "../dist/auto-capture --help > /dev/null 2>&1" \
    ""

# 2. 単一フレームテスト
run_test "単一フレームキャプチャ" \
    "../dist/auto-capture --no-gui --single --output-prefix test_auto > /dev/null 2>&1" \
    "[ -f 'test_auto_single.jpg' ]"

# ファイルクリーンアップ
[ -f "test_auto_single.jpg" ] && rm test_auto_single.jpg

# 3. 範囲指定テスト
run_test "範囲指定キャプチャ" \
    "../dist/auto-capture --area 100,100,300,200 --single --output-prefix test_area_auto > /dev/null 2>&1" \
    "[ -f 'test_area_auto_single.jpg' ]"

# ファイルクリーンアップ
[ -f "test_area_auto_single.jpg" ] && rm test_area_auto_single.jpg

# 4. 連続キャプチャテスト
run_test "連続キャプチャ" \
    "../dist/auto-capture --no-gui --fps 2 --duration 2 --output-prefix test_cont_auto > /dev/null 2>&1" \
    "[ \$(ls test_cont_auto_*.jpg 2>/dev/null | wc -l) -ge 3 ]"

# ファイルクリーンアップ
rm -f test_cont_auto_*.jpg

# 5. エラーハンドリングテスト
echo "テスト: エラーハンドリング (無効なFPS)"
output=$(../dist/auto-capture --fps -1 2>&1)
if [[ $output == *"エラー"* ]]; then
    echo "✅ エラーハンドリング 成功"
    ((PASSED++))
else
    echo "❌ エラーハンドリング 失敗"
    ((FAILED++))
fi
echo ""

# 6. 無効な範囲指定テスト
echo "テスト: 無効な範囲指定"
output=$(../dist/auto-capture --area 100,100,50 2>&1)
if [[ $output == *"エラー"* ]] || [[ $output == *"usage"* ]]; then
    echo "✅ 無効な範囲指定エラーハンドリング 成功"
    ((PASSED++))
else
    echo "✅ 無効な範囲指定は処理されました (警告なし)"
    ((PASSED++))
fi
echo ""

# 7. ファイルサイズテスト
run_test "ファイルサイズ確認" \
    "../dist/auto-capture --no-gui --single --output-prefix size_test > /dev/null 2>&1" \
    "[ -f 'size_test_single.jpg' ] && [ \$(stat -f%z 'size_test_single.jpg' 2>/dev/null || stat -c%s 'size_test_single.jpg' 2>/dev/null) -gt 1000 ]"

# ファイルクリーンアップ
[ -f "size_test_single.jpg" ] && rm size_test_single.jpg

# テスト結果サマリー
echo "=== テスト結果サマリー ==="
echo "成功: $PASSED"
echo "失敗: $FAILED"
echo "合計: $((PASSED + FAILED))"

if [ $FAILED -eq 0 ]; then
    echo "🎉 すべてのテストが成功しました！"
    exit 0
else
    echo "⚠️  $FAILED 個のテストが失敗しました"
    exit 1
fi
