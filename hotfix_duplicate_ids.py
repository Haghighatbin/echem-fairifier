#!/usr/bin/env python3
"""
Hotfix for Streamlit duplicate element ID error.
Run this to automatically fix the duplicate ID issues.
"""

import re
from pathlib import Path


def fix_ui_components():
    """Fix duplicate IDs in UI components."""

    ui_file = Path("src/echem_fairifier/ui/components.py")

    if not ui_file.exists():
        print(f"❌ File not found: {ui_file}")
        return False

    # Read the file
    with open(ui_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Fix 1: Add unique key to plotly_chart
    old_plotly = r"st\.plotly_chart\(fig, use_container_width=True\)"
    new_plotly = 'st.plotly_chart(fig, use_container_width=True, key=f"plot_{technique}_{hash(str(df.columns))}")'
    content = re.sub(old_plotly, new_plotly, content)

    # Fix 2: Add unique key to dataframe
    old_dataframe = r"st\.dataframe\(df\.head\(10\)\)"
    new_dataframe = 'st.dataframe(df.head(10), key=f"dataframe_{technique}_{hash(str(df.shape))}")'
    content = re.sub(old_dataframe, new_dataframe, content)

    # Write back
    with open(ui_file, "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ Fixed UI components duplicate IDs")
    return True


def fix_main_app():
    """Fix duplicate IDs in main app."""

    app_file = Path("src/echem_fairifier/app.py")

    if not app_file.exists():
        print(f"❌ File not found: {app_file}")
        return False

    # Read the file
    with open(app_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Fix: Replace hardcoded CV preview with simple preview
    old_preview = """# Show data preview
                ui.render_data_preview(df, "CV")  # Default to CV for preview"""

    new_preview = """# Show data preview (will be updated with correct technique in Tab 2)
                with st.expander("📊 Quick Data Preview"):
                    st.write(f"**Rows:** {len(df)} | **Columns:** {len(df.columns)}")
                    st.write("**Column names:**", list(df.columns))
                    if len(df) > 0:
                        st.dataframe(df.head(5))"""

    content = content.replace(old_preview, new_preview)

    # Write back
    with open(app_file, "w", encoding="utf-8") as f:
        f.write(content)

    print("✅ Fixed main app duplicate IDs")
    return True


def main():
    """Run all fixes."""
    print("🔧 EChem FAIRifier - Hotfix for Duplicate Element IDs\n")

    fixes_applied = 0

    if fix_ui_components():
        fixes_applied += 1

    if fix_main_app():
        fixes_applied += 1

    print(f"\n📊 Applied {fixes_applied}/2 fixes")

    if fixes_applied == 2:
        print("🎉 All fixes applied! Try running the app again:")
        print("  streamlit run run_app.py")
    else:
        print("⚠️ Some fixes failed. You may need to apply them manually.")


if __name__ == "__main__":
    main()
