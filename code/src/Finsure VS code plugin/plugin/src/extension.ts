import * as vscode from "vscode";
import { exec } from "child_process";
import * as path from "path";
import * as fs from "fs";

export function activate(context: vscode.ExtensionContext) {
  console.log("Testing Hackathon extension activated!");

  const runStreamlit = (content: string, isFile: boolean) => {
    if (!content) {
      vscode.window.showErrorMessage("No content provided.");
      return;
    }

    // Ensure the correct absolute path to dummy.py
    const dummyPath = path.join(context.extensionPath, "scripts", "dummy.py");
    console.log(`✅ Dummy.py Path: ${dummyPath}`);

    vscode.window.showInformationMessage(
      `Running Streamlit with ${isFile ? "file" : "selected text"}`
    );

    // Escape special characters and preserve newlines
    const escapedContent = content.replace(/"/g, '\\"').replace(/\n/g, "\\n");

    // Pass the content as a single argument
    const command = `python -m streamlit run "${dummyPath}" -- "${escapedContent}" --server.port 8500`;
    console.log(`🛠 Running command: ${command}`);

    exec(command, { cwd: context.extensionPath }, (error, stdout, stderr) => {
      if (error) {
        vscode.window.showErrorMessage(`Error: ${error.message}`);
        console.error(`❌ Execution Error: ${error.message}`);
        return;
      }
      console.log(`📜 Streamlit Output: ${stdout}`);
    });
  };

  const paymentapi = async () => {
    const outputChannel = vscode.window.createOutputChannel('Docker Compose Logs');
    outputChannel.show(true);

    try {
        outputChannel.appendLine('Starting Docker Compose...');
        
        // Get the correct scripts path for both dev and production
        const scriptsPath = getScriptsPath(context);
        outputChannel.appendLine(`Resolved scripts path: ${scriptsPath}`);

        // Verify docker-compose.yml exists
        const composePath = path.join(scriptsPath, 'docker-compose.yml');
        if (!fs.existsSync(composePath)) {
            throw new Error(`docker-compose.yml not found at ${composePath}`);
        }

        // Get the full Docker environment
        const dockerEnv = await getDockerEnvironment();

        // Run docker compose
        const command = 'docker-compose up --build';
        outputChannel.appendLine(`Executing: ${command} in ${scriptsPath}`);

        const child = exec(command, {
            cwd: scriptsPath,
            env: dockerEnv,
            maxBuffer: 1024 * 1024 * 10 // 10MB buffer
        });

        // Output handling (keep your existing code)
        child.stdout?.on('data', (data) => {
            outputChannel.append(data);
            if (data.includes('Application running')) {
                openBrowser();
            }
        });

        child.stderr?.on('data', (data) => {
            outputChannel.append(`ERROR: ${data}`);
        });

        child.on('close', (code) => {
            if (code !== 0) {
                outputChannel.appendLine(`Docker failed with code ${code}`);
                vscode.window.showErrorMessage(
                    `Docker Compose failed. Check output for details.`,
                    'Open Output'
                ).then(selection => {
                    if (selection === 'Open Output') outputChannel.show();
                });
            }
        });

        // Cleanup
        context.subscriptions.push(new vscode.Disposable(() => {
            child.kill();
            outputChannel.dispose();
        }));

    } catch (error) {
        const errorMsg = error instanceof Error ? error.message : String(error);
        outputChannel.appendLine(`FATAL ERROR: ${errorMsg}`);
        vscode.window.showErrorMessage(`Failed to start Docker: ${errorMsg}`, 'View Logs')
            .then(selection => {
                if (selection === 'View Logs') outputChannel.show();
            });
    }
};

// Helper function to get the correct scripts path
function getScriptsPath(context: vscode.ExtensionContext): string {
    // First try the normal development path
    const devPath = path.join(context.extensionPath, 'scripts');
    if (fs.existsSync(path.join(devPath, 'docker-compose.yml'))) {
        return devPath;
    }

    // For VSIX package, try the unpacked location
    const vsixPath = path.join(context.extensionPath, 'out', 'scripts');
    if (fs.existsSync(path.join(vsixPath, 'docker-compose.yml'))) {
        return vsixPath;
    }

    // Fallback to extension path
    return context.extensionPath;
}

// Helper function to get Docker environment
async function getDockerEnvironment(): Promise<NodeJS.ProcessEnv> {
    const env = {...process.env};
    
    // On macOS/Linux, ensure PATH includes Docker
    if (process.platform !== 'win32') {
        try {
            const dockerPath = (await execAsync('which docker')).trim();
            env.PATH = `${process.env.PATH}:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin`;
            if (dockerPath) {
                env.PATH = `${path.dirname(dockerPath)}:${env.PATH}`;
            }
        } catch (e) {
            // Ignore errors, use default PATH
        }
    }

    // Add Docker-specific variables
    env.DOCKER_BUILDKIT = '1';
    env.COMPOSE_DOCKER_CLI_BUILD = '1';
    
    return env;
}

// Helper for async exec
function execAsync(command: string): Promise<string> {
    return new Promise((resolve, reject) => {
        exec(command, (error, stdout, stderr) => {
            if (error) reject(error);
            else resolve(stdout.toString());
        });
    });
}
  
  // Helper function to open browser
  function openBrowser() {
    const url = 'http://localhost:8501';
    console.log(`🌐 Opening browser to: ${url}`);
    vscode.env.openExternal(vscode.Uri.parse(url));
  }

  const creditrisk = () => {

    // Ensure the correct absolute path to dummy.py
    const creditriskPath = path.join(context.extensionPath, "scripts", "generation.py");

    vscode.window.showInformationMessage(
      `Running Streamlit for Credit Risk Analysis Testing`
    );

    // Pass the content as a single argument
    const command = `python "${creditriskPath}"`;
    console.log(`🛠 Running command: ${command}`);

    exec(command, { cwd: context.extensionPath }, (error, stdout, stderr) => {
      if (error) {
        vscode.window.showErrorMessage(`Error: ${error.message}`);
        console.error(`❌ Execution Error: ${error.message}`);
        return;
      }
      console.log(`📜 Output: ${stdout}`);
    });
  };

  const regulatorycompliance = (filePath: string) => {
    if (!filePath) {
        vscode.window.showErrorMessage("No file selected.");
        return;
    }

    // Path to glue.py in your extension's scripts folder
    const glueScriptPath = path.join(context.extensionPath, "scripts", "glue.py");
    console.log(`[DEBUG] glue.py path: ${glueScriptPath}`);

    // Run: python glue.py "<filePath>"
    const command = `python "${glueScriptPath}" "${filePath}"`;
    console.log(`[DEBUG] Executing: ${command}`);

    // Execute the command
    exec(command, { cwd: context.extensionPath }, (error, stdout, stderr) => {
        if (error) {
            console.error(`[ERROR] ${error.message}`);
            vscode.window.showErrorMessage(`Compliance check failed: ${error.message}`);
            return;
        }
        if (stderr) {
            console.error(`[ERROR] ${stderr}`);
        }
        console.log(`[OUTPUT] ${stdout}`);
        vscode.window.showInformationMessage("Compliance check completed!");
    });
};

  const chatbottesting = () => {
    // Ensure the correct absolute path to chatbot_testing.py
    const chatbotPath = path.join(context.extensionPath, "scripts", "chatbot_testing.py");
    console.log(`✅ chatbot_testing.py Path: ${chatbotPath}`);

    // Pass the content as a single argument
    const command = `python -m streamlit run "${chatbotPath}"  --server.port 8521`;
    console.log(`🛠 Running command: ${command}`);

    exec(command, { cwd: context.extensionPath }, (error, stdout, stderr) => {
      if (error) {
        vscode.window.showErrorMessage(`Error: ${error.message}`);
        console.error(`❌ Execution Error: ${error.message}`);
        return;
      }
      console.log(`📜 Streamlit Output: ${stdout}`);
    });
  };

  const uitesting = () => {
    // Ensure the correct absolute path to chatbot_testing.py
    const uiPath = path.join(context.extensionPath, "scripts", "ui_testing.py");
    console.log(`✅ ui_testing.py Path: ${uiPath}`);

    // Pass the content as a single argument
    const command = `python -m streamlit run "${uiPath}" --server.port 8511`;
    console.log(`🛠 Running command: ${command}`);

    exec(command, { cwd: context.extensionPath }, (error, stdout, stderr) => {
      if (error) {
        vscode.window.showErrorMessage(`Error: ${error.message}`);
        console.error(`❌ Execution Error: ${error.message}`);
        return;
      }
      console.log(`📜 Streamlit Output: ${stdout}`);
    });
  };

  // Register commands for Explorer context menu (file right-click)
  let command1 = vscode.commands.registerCommand(
    `finsure.fileOption${1}`,
    (fileUri: vscode.Uri) => {
      // Read the entire file content
      const filePath = fileUri.fsPath;
      const fileContent = fs.readFileSync(filePath, "utf-8");
      paymentapi();
    }
  );
  context.subscriptions.push(command1);

  let command2 = vscode.commands.registerCommand(
    `finsure.fileOption${2}`,
    (fileUri: vscode.Uri) => {
      // Read the entire file content
      const filePath = fileUri.fsPath;
      const fileContent = fs.readFileSync(filePath, "utf-8");
      creditrisk();
    }
  );
  context.subscriptions.push(command2);
  
  let command3 = vscode.commands.registerCommand(
    `finsure.fileOption${3}`,
    (fileUri: vscode.Uri) => {
        // Pass the file path directly (no need to read content here)
        const filePath = fileUri.fsPath;
        regulatorycompliance(filePath);
    }
  );
  context.subscriptions.push(command3);

  let command4 = vscode.commands.registerCommand(
    `finsure.fileOption${4}`,
    () => {
      chatbottesting();
    }
  );
  context.subscriptions.push(command4);

  let command5 = vscode.commands.registerCommand(
    `finsure.fileOption${5}`,
    () => {
      uitesting();
    }
  );
  context.subscriptions.push(command5);


  // Register commands for Editor context menu (text selection)
  let command6 = vscode.commands.registerCommand(
    `finsure.selectionOption${1}`,
    () => {
      const editor = vscode.window.activeTextEditor;
      if (editor) {
        const selection = editor.document.getText(editor.selection);
        paymentapi();
      } else {
        vscode.window.showErrorMessage("No active editor found.");
      }
    }
  );
  context.subscriptions.push(command6);

  let command7 = vscode.commands.registerCommand(
    `finsure.selectionOption${2}`,
    () => {
      const editor = vscode.window.activeTextEditor;
      if (editor) {
        const selection = editor.document.getText(editor.selection);
        creditrisk();
      } else {
        vscode.window.showErrorMessage("No active editor found.");
      }
    }
  );
  context.subscriptions.push(command7);

  // let command8 = vscode.commands.registerCommand(
  //   `finsure.selectionOption${3}`,
  //   () => {
  //     const editor = vscode.window.activeTextEditor;
  //     if (editor) {
  //       const selection = editor.document.getText(editor.selection);
  //       runStreamlit(selection, false);
  //     } else {
  //       vscode.window.showErrorMessage("No active editor found.");
  //     }
  //   }
  // );
  // context.subscriptions.push(command8);

  let command9 = vscode.commands.registerCommand(
    `finsure.selectionOption${4}`,
    () => {
      const editor = vscode.window.activeTextEditor;
      if (editor) {
        chatbottesting();
      } else {
        vscode.window.showErrorMessage("No active editor found.");
      }
    }
  );
  context.subscriptions.push(command9);

  let command10 = vscode.commands.registerCommand(
    `finsure.selectionOption${5}`,
    () => {
      const editor = vscode.window.activeTextEditor;
      if (editor) {
        const selection = editor.document.getText(editor.selection);
        uitesting();
      } else {
        vscode.window.showErrorMessage("No active editor found.");
      }
    }
  );
  context.subscriptions.push(command10);
}

export function deactivate() {}