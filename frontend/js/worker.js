/**
 * AlgoGround Web Worker Code Execution Sandbox
 * Runs arbitrary candidate algorithms in an isolated thread.
 * Captures stdout, intercepts runtime exceptions, and shields main UI thread.
 */

self.onmessage = function (e) {
    const { code, functionName, testCases } = e.data;
    const logs = [];

    // Intercept console.log inside the sandbox
    const originalLog = console.log;
    console.log = function (...args) {
        logs.push(args.map(a => (typeof a === 'object' ? JSON.stringify(a) : String(a))).join(' '));
    };

    try {
        const startTime = performance.now();
        
        // Evaluate user function inside sandbox
        const factory = new Function(`
            ${code}
            if (typeof ${functionName} !== 'undefined') {
                return ${functionName};
            }
            return null;
        `);

        const userFn = factory();
        if (typeof userFn !== 'function') {
            throw new Error(`Function '${functionName}' was not defined in your code.`);
        }

        const results = [];
        let allPassed = true;

        for (const tc of testCases) {
            const tcStart = performance.now();
            let actual = null;
            let passed = false;
            let error = null;

            try {
                // Determine parameter invocation
                if (Array.isArray(tc.input)) {
                    actual = userFn(...tc.input);
                } else if (typeof tc.input === 'object' && tc.input !== null) {
                    actual = userFn(...Object.values(tc.input));
                } else {
                    actual = userFn(tc.input);
                }

                // Check deep equality
                const actualStr = JSON.stringify(actual);
                const expectedStr = JSON.stringify(tc.expected_output);
                passed = (actualStr === expectedStr);
            } catch (err) {
                error = err.message || String(err);
                passed = false;
            }

            if (!passed) allPassed = false;

            results.push({
                test_case_id: tc.id,
                passed,
                input: tc.input,
                expected_output: tc.expected_output,
                actual_output: actual,
                runtime_ms: +(performance.now() - tcStart).toFixed(2),
                error
            });
        }

        const totalRuntime = +(performance.now() - startTime).toFixed(2);

        self.postMessage({
            success: true,
            status: allPassed ? "Accepted" : "Wrong Answer",
            results,
            stdout: logs.join('\n'),
            runtime_ms: totalRuntime
        });

    } catch (fatalError) {
        self.postMessage({
            success: false,
            status: "Runtime Error",
            error: fatalError.message || String(fatalError),
            stdout: logs.join('\n'),
            results: []
        });
    } finally {
        console.log = originalLog;
    }
};
