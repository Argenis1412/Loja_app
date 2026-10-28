import { PagamentoForm } from '../components/PagamentoForm';

export function StepPagamento() {
  return (
    <div className="mx-auto max-w-md space-y-6 p-6">
      <header className="text-center">
        <h1 className="text-2xl font-semibold">Loja Argenis Lopez</h1>
        <p className="text-sm text-gray-500">
          Informe os dados para simular o pagamento
        </p>
      </header>

      <PagamentoForm />
    </div>
  );
}
