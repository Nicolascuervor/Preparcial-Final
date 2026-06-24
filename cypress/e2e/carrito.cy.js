describe('Pruebas E2E del Carrito de Compras', () => {
  it('Debe agregar un producto y mostrar el total correctamente', () => {
    cy.visit('http://localhost:4200/carrito');
    cy.get('[data-testid="input-nombre-producto"]').type('Monitor');
    cy.get('[data-testid="input-precio-producto"]').type('1500000');
    cy.get('[data-testid="input-cantidad-producto"]').type('1');
    cy.get('[data-testid="btn-agregar-producto"]').click();
    cy.get('[data-testid="total-carrito"]')
      .should('be.visible')
      .and('contain', '1.500.000');
  });
});
