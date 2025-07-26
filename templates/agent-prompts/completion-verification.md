# Agent Instructions: Story Completion Verification

## 🚨 CRITICAL REQUIREMENT

**You MUST verify all work is complete before marking any story as done. False completion claims will be detected and rejected.**

---

## ✅ Step-by-Step Verification Process

### 1. Pre-Completion Checklist
Before even considering marking a story complete, verify:
- [ ] All code changes are implemented
- [ ] All tests are passing
- [ ] No new technical debt introduced
- [ ] Documentation is updated
- [ ] Code follows project standards

### 2. Run Primary Validation
```bash
# This is your MANDATORY validation command
./scripts/validation/story-completion-validator.sh --story=X.Y --validate-completion

# Or with AVAAD v2 (when available):
avaad validate story-X.Y --explain
```

**The validation MUST show "PASS" or "VERIFIED_COMPLETE"**

### 3. Check Technical Debt
```bash
# Ensure no regression in technical debt
./scripts/validation/technical-debt-gate-check.sh --pr-mode

# Or with AVAAD v2:
avaad check-debt
```

**Current baseline: 49 MyPy errors (do not exceed)**

### 4. Provide Proof of Completion
When claiming a story is complete, you MUST provide:

```markdown
## Story X.Y Completion Evidence

**Validation Results:**
```
[PASTE FULL OUTPUT OF: ./scripts/validation/story-completion-validator.sh --story=X.Y --validate-completion]
```

**Technical Debt Check:**
```
[PASTE OUTPUT OF: ./scripts/validation/technical-debt-gate-check.sh --pr-mode]
```

**Test Results:**
```
[PASTE OUTPUT OF: make test]
```

**Files Modified:**
- file1.py (what was changed)
- file2.py (what was changed)
- etc.

**MyPy Status:**
- Before: X errors
- After: Y errors
- Target: ≤ baseline (49)
```

---

## 🛑 What Will Cause Rejection

Your completion claim will be AUTOMATICALLY REJECTED if:

1. **No validation output provided** - We need proof, not promises
2. **Validation shows FAIL** - The work isn't actually done
3. **Technical debt increased** - You introduced new problems
4. **Tests are failing** - The code doesn't work
5. **Missing files** - You didn't complete all required changes

---

## 💡 Common Scenarios

### Scenario: "MyPy Errors Remain"
```bash
# If validation shows MyPy errors in files you claim are fixed:
❌ Story 6.2 validation failed
   - core/logging.py: 4 errors
   - core/business_metrics.py: 2 errors

# YOU MUST:
1. Fix ALL errors in the listed files
2. Re-run validation until it passes
3. Only then mark as complete
```

### Scenario: "Tests Are Failing"
```bash
# If any tests fail:
FAILED tests/unit/test_logging.py::test_structured_logging

# YOU MUST:
1. Fix the failing tests
2. Ensure all tests pass
3. Re-run validation
```

### Scenario: "New Technical Debt"
```bash
# If technical debt check shows regression:
❌ MyPy error count increased (52 > 49)

# YOU MUST:
1. Fix the new errors you introduced
2. Get count back to or below baseline
3. Re-run validation
```

---

## 📋 Quick Commands Reference

### For MyPy/Type Safety Stories
```bash
# Check specific file passes strict mode
poetry run mypy path/to/file.py --strict

# Check overall error count
poetry run mypy apps/api/src packages/db --strict 2>&1 | grep -c "error:"

# Run story validation
./scripts/validation/mypy-story-validator.sh --story=X.Y --story-file=docs/stories/X.Y.story.md
```

### For Database Stories
```bash
# Test migrations
poetry run alembic upgrade head
poetry run alembic downgrade -1

# Validate database story
./scripts/validation/database-story-validator.sh --story=X.Y --story-file=docs/stories/X.Y.story.md
```

### For All Story Types
```bash
# Primary validation (ALWAYS RUN THIS)
./scripts/validation/story-completion-validator.sh --story=X.Y --validate-completion

# Generate completion report
make validate-story STORY=X.Y
```

---

## 🎯 Remember

1. **Validation is not optional** - It's a mandatory requirement
2. **Proof is required** - Always paste the full validation output
3. **False claims are detected** - The CI/CD pipeline will catch lies
4. **Fix before marking complete** - Don't mark complete and plan to fix later

---

## 📝 Example: Correct Completion Claim

```markdown
I have completed Story 6.2. Here is my verification:

**Validation Output:**
```bash
$ ./scripts/validation/story-completion-validator.sh --story=6.2 --validate-completion
🔍 Validating Story 6.2 completion status...
✅ Story type detected: mypy_story
✅ MyPy validation: PASSED
✅ Technical debt check: PASSED (49 errors, no regression)
✅ All tests: PASSED
✅ Documentation: Updated

RESULT: Story 6.2 is VERIFIED COMPLETE
```

**All required files have been fixed and pass MyPy strict mode.**
```

This is the level of proof required for every story completion claim.
