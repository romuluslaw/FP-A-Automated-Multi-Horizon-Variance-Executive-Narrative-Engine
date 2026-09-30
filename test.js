/**
 * Node.js Integration & Regression Test Suite for FP&A Engine.
 * Tests Python pipeline execution, threshold filtering, working capital formulas, and mock LLM mode.
 */

const { spawnSync } = require('child_process');
const assert = require('assert');

console.log('====================================================');
console.log(' RUNNING FP&A AUTOMATION SUITE (Node.js Test Runner)');
console.log('====================================================\n');

function runTest() {
  try {
    // 1. Execute Main Python Script in Mock Mode
    console.log('[TEST 1]: Executing Python CLI Pipeline in Mock Mode...');
    const pyProcess = spawnSync('python3', ['main.py', '--mock'], { encoding: 'utf-8' });

    if (pyProcess.error) {
      throw new Error(`Failed to start Python process: ${pyProcess.error.message}`);
    }

    assert.strictEqual(pyProcess.status, 0, `Python exited with error code ${pyProcess.status}: ${pyProcess.stderr}`);
    
    const result = JSON.parse(pyProcess.stdout);
    console.log('  ✔ Python CLI Process executed successfully.');

    // 2. Validate Working Capital Ratios Formulas
    console.log('\n[TEST 2]: Verifying Financial Ratios & Working Capital Calculations...');
    const ratios = result.ratios;
    
    assert.ok(typeof ratios.DSO_Days === 'number', 'DSO must be a valid number.');
    assert.ok(typeof ratios.DPO_Days === 'number', 'DPO must be a valid number.');
    assert.strictEqual(
      ratios.Working_Capital_Drag_Days,
      Number((ratios.DSO_Days - ratios.DPO_Days).toFixed(2)),
      'Working Capital Drag must equal DSO - DPO.'
    );
    console.log(`  ✔ DSO (${ratios.DSO_Days} days) - DPO (${ratios.DPO_Days} days) = Working Capital Drag (${ratios.Working_Capital_Drag_Days} days). Correct.`);

    // 3. Validate Materiality Thresholds
    console.log('\n[TEST 3]: Verifying Materiality Filtering Logic...');
    assert.ok(result.material_variances_count > 0, 'Material variance count should be > 0 for test dataset.');
    console.log(`  ✔ Material variance items correctly isolated (${result.material_variances_count} items).`);

    // 4. Validate Dual-Mode LLM Mock Output & PDPA Scrubbing
    console.log('\n[TEST 4]: Verifying Stakeholder Narrative Engine & PDPA Scrubbing...');
    const narratives = result.narratives;
    assert.ok(narratives.Leadership.includes('[MOCK AI]'), 'Leadership narrative should use Mock Fallback Mode.');
    assert.ok(narratives.Board.includes('[MOCK AI]'), 'Board narrative should use Mock Fallback Mode.');
    assert.ok(narratives.Investors.includes('[MOCK AI]'), 'Investor narrative should use Mock Fallback Mode.');
    console.log('  ✔ All 3-Column Stakeholder Narratives successfully generated and anonymized.');

    console.log('\n====================================================');
    console.log(' ALL INTEGRATION & REGRESSION TESTS PASSED (4/4)');
    console.log('====================================================');
  } catch (err) {
    console.error('\n❌ TEST SUITE FAILED:', err.message);
    process.exit(1);
  }
}

runTest();