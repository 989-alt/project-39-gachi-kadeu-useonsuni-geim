"""End-to-end smoke + flow test for 가치 카드 우선순위 게임 (#039).

Runs against http://127.0.0.1:5180 — server is launched by with_server.py.
"""
import sys
import pathlib
from playwright.sync_api import sync_playwright, expect

ROOT = pathlib.Path(__file__).resolve().parent.parent
SHOTS = ROOT / "screenshots"
SHOTS.mkdir(parents=True, exist_ok=True)


def main() -> int:
    console_errors: list[str] = []
    page_errors: list[str] = []
    failed_requests: list[str] = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            viewport={"width": 1280, "height": 900},
            device_scale_factor=2,
        )
        page = ctx.new_page()

        page.on("console", lambda m: console_errors.append(m.text) if m.type == "error" else None)
        page.on("pageerror", lambda e: page_errors.append(str(e)))
        page.on("requestfailed",
                lambda r: failed_requests.append(f"{r.url} :: {r.failure}"))

        page.goto("http://127.0.0.1:5180/index.html")
        page.wait_for_load_state("networkidle")

        # === Stage 1 ===
        expect(page.locator("#stageTitle")).to_have_text("지금 너에게 더 중요한 가치는?")
        expect(page.locator("#progressPill")).to_contain_text("1 / 3")
        expect(page.locator(".card")).to_have_count(10)
        page.screenshot(path=str(SHOTS / "01-stage1-initial.png"), full_page=True)

        # Capture initial top card
        initial_top = page.locator(".card").first.get_attribute("data-id")

        # Move 2nd card up via ↑ button — it should become rank 1
        second_id = page.locator(".card").nth(1).get_attribute("data-id")
        page.locator(".card").nth(1).locator("button[aria-label='순위 한 칸 올리기']").click()
        new_top = page.locator(".card").first.get_attribute("data-id")
        assert new_top == second_id, f"Move-up failed: top={new_top}, expected={second_id}"

        # Expand description on click
        page.locator(".card").first.click()
        expect(page.locator(".card").first.locator(".card-desc")).to_be_visible()

        # Keyboard nav: focus first card, press ArrowDown → it should drop to rank 2
        page.locator(".card").first.focus()
        page.keyboard.press("ArrowDown")
        moved_id = page.locator(".card").first.get_attribute("data-id")
        assert moved_id != new_top, "ArrowDown did not move card"
        page.screenshot(path=str(SHOTS / "02-stage1-after-keyboard.png"), full_page=True)

        # Advance to stage 2
        page.locator("#nextBtn").click()
        expect(page.locator("#stageTitle")).to_have_text("이 5개 중 정말 중요한 건?")
        expect(page.locator("#progressPill")).to_contain_text("2 / 3")
        expect(page.locator(".card")).to_have_count(5)
        page.screenshot(path=str(SHOTS / "03-stage2.png"), full_page=True)

        # Memo input
        page.locator("#memoText").fill("이 5개가 가장 자주 떠올랐어요.")
        expect(page.locator("#memoCount")).to_contain_text("/ 120")

        # Test "이전 단계" back to stage 1
        page.locator("#prevBtn").click()
        expect(page.locator("#progressPill")).to_contain_text("1 / 3")
        # Forward again — memo should persist
        page.locator("#nextBtn").click()
        expect(page.locator("#memoText")).to_have_value("이 5개가 가장 자주 떠올랐어요.")

        # Advance to stage 3
        page.locator("#nextBtn").click()
        expect(page.locator("#stageTitle")).to_have_text("너의 TOP 3 가치")
        expect(page.locator("#progressPill")).to_contain_text("3 / 3")
        expect(page.locator(".card")).to_have_count(3)
        # 1위 dark surface card
        rank1 = page.locator(".card.rank-1")
        expect(rank1).to_have_count(1)
        page.screenshot(path=str(SHOTS / "04-stage3-final.png"), full_page=True)

        # Final memo
        page.locator("#memoText").fill("정직은 어떤 상황에서도 내 마음의 기준이 돼요.")

        # PNG export — intercept download
        with page.expect_download() as dl_info:
            page.locator("#nextBtn").click()
        download = dl_info.value
        out_png = SHOTS / "05-export-result.png"
        download.save_as(str(out_png))
        assert out_png.exists() and out_png.stat().st_size > 5000, \
            f"PNG export tiny or missing: {out_png.stat().st_size if out_png.exists() else 'missing'}"

        # Reset flow — open the modal from stage 3
        page.locator("#prevBtn").click()
        expect(page.locator("#resetModal")).to_be_visible()
        page.locator("#resetConfirm").click()
        expect(page.locator("#resetModal")).to_be_hidden()
        expect(page.locator("#progressPill")).to_contain_text("1 / 3")
        expect(page.locator(".card")).to_have_count(10)

        # Mobile viewport sanity
        page.set_viewport_size({"width": 380, "height": 720})
        page.screenshot(path=str(SHOTS / "06-mobile-stage1.png"), full_page=True)
        # Tap target should still work
        page.locator(".card").nth(2).locator("button[aria-label='순위 한 칸 올리기']").click()

        browser.close()

    # ENV NOISE filter — favicon 404 from http.server is fine; CDN warnings etc.
    real_failed = [r for r in failed_requests if "favicon" not in r.lower()]

    print("=" * 60)
    print(f"Console errors : {len(console_errors)}")
    for e in console_errors: print(f"  - {e}")
    print(f"Page errors    : {len(page_errors)}")
    for e in page_errors:    print(f"  - {e}")
    print(f"Failed requests: {len(real_failed)} (after env-noise filter)")
    for r in real_failed:    print(f"  - {r}")
    print("=" * 60)

    hard_fail = console_errors or page_errors or real_failed
    return 1 if hard_fail else 0


if __name__ == "__main__":
    sys.exit(main())
