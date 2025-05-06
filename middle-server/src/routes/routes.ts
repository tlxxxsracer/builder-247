import { Router, RequestHandler } from "express";
import { verifyBearerToken } from "../middleware/auth";
import { validateSignature, getSignatureGenerationDocs } from "../middleware/signature_validation";
import { ValidateRoute } from "../middleware/route_validator";

// Import all existing route handlers
/******** Builder *********/
import { fetchTodo } from "../controllers/builder/fetchToDo";
import { addPR } from "../controllers/builder/addTodoPR";
import { checkToDo } from "../controllers/builder/checkToDo";
import { updateAuditResult } from "../controllers/builder/updateAuditResult";
import { addAggregatorInfo } from "../controllers/builder/addAggregatorInfo";
import { addIssuePR } from "../controllers/builder/addIssuePR";
import { assignIssue } from "../controllers/builder/assignIssue";
import { fetchIssue } from "../controllers/builder/fetchIssue";
import { checkIssue } from "../controllers/builder/checkIssue";
import { getSourceRepo } from "../controllers/builder/getSourceRepo";

// Other imports...

const router = Router();

// Documentation route for signature generation
router.get("/docs/signature-generation", (req, res) => {
  res.json(getSignatureGenerationDocs());
});

// Public routes
router.get("/hello", (req, res) => {
  res.json({ message: "Hello World!" });
});

// Routes with signature validation
/********** Builder ***********/
router.post("/builder/fetch-to-do", validateSignature, fetchTodo as RequestHandler);
router.post("/builder/add-aggregator-info", validateSignature, addAggregatorInfo as RequestHandler);
router.post("/builder/add-pr-to-to-do", validateSignature, addPR as RequestHandler);
router.post("/builder/add-issue-pr", validateSignature, addIssuePR as RequestHandler);
router.post("/builder/check-to-do", validateSignature, checkToDo as RequestHandler);
router.post("/builder/assign-issue", validateSignature, assignIssue as RequestHandler);
router.post("/builder/update-audit-result", validateSignature, updateAuditResult as RequestHandler);
router.post("/builder/fetch-issue", validateSignature, fetchIssue as RequestHandler);
router.post("/builder/check-issue", validateSignature, checkIssue as RequestHandler);
router.get("/builder/get-source-repo/:nodeType/:uuid", validateSignature, getSourceRepo as RequestHandler);

// Maintain existing authentication methods
router.post("/prometheus/classification", verifyBearerToken, validateSignature, (req, res) => {
  // Existing classification logic
});

export default router;