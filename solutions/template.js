import {promises as fs} from 'fs';
import * as parser from '@babel/parser';
import * as t from "@babel/types";
import _traverse from '@babel/traverse';
import _generate from '@babel/generator';

const traverse = _traverse.default;
const generate = _generate.default;


/*
 * Generate and prettify source code from the AST
 */
function generateCode(ast) {
    return generate(ast, {
        comments: false,
        compact: false,
    }).code;
}


/*
 * Replace constants by the string value
 */
function constantUnfolding(source) {
    // Convert source code to an AST (Abstract Syntax Tree)
    const ast = parser.parse(source);

    // Replace variable usage by their string declaration
    traverse(ast, {
        VariableDeclaration(path) {
            // TO FILL
        }
    });

    // Replace the binding of the window usage
    traverse(ast, {
        VariableDeclaration(path) {
            // TO FILL
        }
    });

    return generateCode(ast);
}

/*
 * Join binary expressions with string literals
 */
function stringJoin(source) {
    // Convert source code to an AST (Abstract Syntax Tree)
    const ast = parser.parse(source);

    function joinBinaryWithStringRecursively(node) {
        // TO REPLACE
        return node;
    }

    // Replace binary expressions by their string concatenation
    // Use a recursive function
    traverse(ast, {
        BinaryExpression(path) {
            const node = path.node;

            path.replaceWith(joinBinaryWithStringRecursively(node));
        }
    });

    return generateCode(ast);
}

/*
 * Convert the string notation to the dot notation
 */
function convertStringNotationToDotNotation(source) {
    // Convert source code to an AST (Abstract Syntax Tree)
    const ast = parser.parse(source);

    traverse(ast, {
        MemberExpression(path) {
            // TO FILL
        }
    });

    return generateCode(ast);
}


(async () => {
    let code = await fs.readFile('./tools/obfuscated.js', 'utf-8');

    code = constantUnfolding(code);
    code = stringJoin(code);
    code = convertStringNotationToDotNotation(code);

    await fs.writeFile('./tools/deobfuscated.js', code, 'utf-8');
})()
    .catch(console.error);
